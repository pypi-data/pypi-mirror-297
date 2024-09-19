from pathlib import Path
from typing import Generator

import torch
from matchms import Spectrum
from torch.nn import Transformer

from .model.generative import CSTseq, tkn
from .utils.spectra import tensorize_peaks


class Predictor:
    def __init__(self, ckpt: str | Path = Path(__file__).parent / "ckpt" / "seq.ckpt", device: str = "cpu"):
        """
        Initialize the Predictor
        :param ckpt: Path to the model checkpoint file
        :param device: Device to run the model on ('cpu' or 'cuda')
        """
        ckpt = Path(ckpt)
        self.device = device
        self.seq = CSTseq.load_from_checkpoint(ckpt).eval().to(self.device)

    def _make_peaks(self, spec: Spectrum):
        """
        Process the spectrum peaks and move the tensor to the correct device.
        """
        return tensorize_peaks(
            spec.peak_comments,
            spec.peaks.intensities,
            spec.get("formula"),
            spec.get("adduct")
        ).float().unsqueeze(1).to(self.device)

    def _generate_lookahead_mask(self, size: int) -> torch.Tensor:
        """
        Generate a look-ahead mask for the transformer decoder.
        """
        return Transformer.generate_square_subsequent_mask(size).to(self.device)

    @torch.no_grad()
    def _beam_search_decode(self, embedding, hint, max_len, beam_width, alpha):
        eos_id = tkn.token_to_id("</s>")
        # Initialize sequences
        beam_seq = hint  # Shape: (seq_len, 1)
        beam_scores = torch.zeros(1, device=self.device)  # Initial scores
        beam_finished = torch.zeros(1, dtype=torch.bool, device=self.device)  # Finished flags

        for _ in range(max_len):
            tgt_mask = self._generate_lookahead_mask(beam_seq.shape[0])
            # Decode the next token probabilities for all beams in parallel
            out = self.seq.decode(
                beam_seq,
                embedding.repeat(1, beam_seq.size(1), 1),
                tgt_mask
            )[-1]  # Shape: (beam_width, vocab_size)
            log_probs = torch.log_softmax(out, dim=-1)

            # Calculate cumulative scores with length normalization
            length_penalty = ((beam_seq.size(0)) ** alpha) / ((beam_seq.size(0) + 1) ** alpha)
            cumulative_scores = beam_scores.unsqueeze(1) + log_probs * length_penalty

            # Flatten and select top beam_width candidates
            cumulative_scores = cumulative_scores.view(-1)
            top_scores, top_indices = torch.topk(cumulative_scores, beam_width)

            # Compute indices for beams and tokens
            beam_indices = top_indices // log_probs.size(1)
            token_indices = top_indices % log_probs.size(1)

            # Update sequences, scores, and finished flags
            new_seq = []
            new_finished = []
            for i in range(beam_width):
                beam_idx = beam_indices[i].item()  # Convert to integer
                token_idx = token_indices[i]
                seq = torch.cat([beam_seq[:, beam_idx], token_idx.view(1)], dim=0)
                new_seq.append(seq)
                is_finished = beam_finished[beam_idx] or (token_idx.item() == eos_id)
                new_finished.append(is_finished)
            beam_seq = torch.stack(new_seq, dim=1)
            beam_scores = top_scores
            beam_finished = torch.tensor(new_finished, device=self.device)

            # Break if all sequences have finished
            if beam_finished.all():
                break

        # Extract sequences and scores
        sequences = [beam_seq[:, i] for i in range(beam_seq.size(1))]
        return list(zip(sequences, beam_scores))

    @torch.no_grad()
    def beam_predict(self, spec: Spectrum, n_beam=5, alpha=0.75) -> list[tuple[str, float]]:
        """
        Predict the SMILES of the given spectrum using beam search algorithm.
        :param spec: Spectrum to be annotated
        :param n_beam: Number of beams to be used
        :param alpha: Length normalization factor
        :return: List of predicted SMILES and their scores
        """
        hint = torch.tensor(
            tkn.encode(spec.get("standard_formula")).ids,
            dtype=torch.long,
            device=self.device
        ).unsqueeze(1)
        peaks = self._make_peaks(spec)
        embedding = self.seq.encode(peaks)
        tgt_tokens = self._beam_search_decode(
            embedding, hint, max_len=200, beam_width=n_beam, alpha=alpha
        )
        results = []
        formula_len = len(spec.get("standard_formula"))
        for indices, score in tgt_tokens:
            tokens = indices.tolist()  # Removed .squeeze(1)
            decoded = tkn.decode(tokens)
            smiles = "".join(decoded.split(" "))[formula_len:]
            results.append((smiles, score.item()))
        return results

    @torch.no_grad()
    def sample_prob(self, spec: Spectrum, smiles: str) -> float:
        """
        Calculate the probability of the given SMILES string given the spectrum.
        :param spec: Spectrum to be annotated
        :param smiles: Candidate SMILES string
        :return: Probability of the SMILES string generated by the model
        """
        tgt_tokens = tkn.encode(spec.get("standard_formula"), smiles)
        tgt_in = torch.tensor(
            tgt_tokens.ids, dtype=torch.long, device=self.device
        ).unsqueeze(1)[:-1]
        tgt_mask = self._generate_lookahead_mask(tgt_in.shape[0])
        peaks = self._make_peaks(spec)
        embedding = self.seq.encode(peaks)
        logits = self.seq.decode(tgt_in, embedding, tgt_mask)
        segment = torch.tensor(tgt_tokens.type_ids, dtype=bool, device=self.device)
        probs = torch.softmax(logits, dim=-1)[segment[1:]].squeeze(1)
        smiles_id = torch.tensor(tgt_tokens.ids, dtype=torch.long, device=self.device)[segment]
        smiles_prob = probs[torch.arange(probs.shape[0]), smiles_id]
        return smiles_prob.mean().item()

    @torch.no_grad()
    def _greedy_decode(self, embedding, hint, max_len):
        """
        Generator for greedy decoding, yielding tokens as they are generated.
        """
        ys = hint
        for _ in range(max_len):
            tgt_mask = self._generate_lookahead_mask(ys.shape[0])
            out = self.seq.decode(ys, embedding, tgt_mask)[-1]
            _, idx = torch.max(out, dim=1)
            ys = torch.cat([ys, idx.view(1, 1)], dim=0)

            # Yield the latest token
            yield idx.view(1, 1)

            # Stop if end token is generated
            if idx.item() == tkn.token_to_id("</s>"):
                break

    @torch.no_grad()
    def greedy_stream(self, spec: Spectrum) -> Generator[str, None, None]:
        """
        Streamed greedy prediction, yielding intermediate SMILES strings.
        :param spec: Spectrum to be annotated.
        :yield: Partially predicted SMILES string at each step
        """
        hint = torch.tensor(
            tkn.encode(spec.get("standard_formula")).ids,
            dtype=torch.long,
            device=self.device
        ).unsqueeze(1)
        peaks = self._make_peaks(spec)
        embedding = self.seq.encode(peaks)
        for step in self._greedy_decode(embedding, hint, max_len=200):
            result = tkn.decode(step.squeeze(1).tolist())
            yield "".join(result.split(" "))

    def __call__(self, spec: Spectrum) -> Generator[str, None, None]:
        """
        Predict the SMILES of the given spectrum using greedy search algorithm.
        :param spec: Spectrum to be annotated
        :yield: Predicted SMILES string
        """
        return self.greedy_stream(spec)

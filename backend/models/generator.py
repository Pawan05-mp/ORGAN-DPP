import torch
import torch.nn as nn
import torch.nn.functional as F
import random

# simple char-level SMILES vocabulary (extend as needed)
SMILES_VOCAB = list("CNOFPSClBrIBr[]()=#123456789+-\\/@\\")
SMILES_VOCAB = list(dict.fromkeys(SMILES_VOCAB))
SMILES_VOCAB.append(".")
SMILES_VOCAB.append(" ")
SMILES_VOCAB = ["<pad>", "<sos>", "<eos>"] + SMILES_VOCAB
IDX = {c: i for i, c in enumerate(SMILES_VOCAB)}


class LSTMGenerator(nn.Module):
    def __init__(self, embed_size=128, hidden_size=512, dropout=0.3, device=None):
        super().__init__()
        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
        self.vocab = SMILES_VOCAB
        self.vocab_size = len(self.vocab)
        self.embed = nn.Embedding(self.vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers=2, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, self.vocab_size)
        self.to(self.device)

    def forward(self, x, hidden=None):
        x = self.embed(x)
        out, hidden = self.lstm(x, hidden)
        logits = self.fc(out)
        return logits, hidden

    def sample_smiles(self, batch_size=64, max_len=120, temperature=1.0):
        self.eval()
        results = []
        with torch.no_grad():
            for _ in range(batch_size):
                inp = torch.tensor([[IDX["<sos>"]]], device=self.device)
                hidden = None
                seq = []
                for _ in range(max_len):
                    logits, hidden = self.forward(inp, hidden)
                    logits = logits[:, -1, :].squeeze(0) / max(1e-6, temperature)
                    probs = F.softmax(logits, dim=-1).cpu().numpy()
                    idx = int(torch.from_numpy(np_random_choice(probs)))
                    token = self.vocab[idx]
                    if token == "<eos>":
                        break
                    if token not in ["<pad>", "<sos>"]:
                        seq.append(token)
                    inp = torch.tensor([[idx]], device=self.device)
                results.append("".join(seq))
        return results


def np_random_choice(probs):
    import numpy as np
    return np.random.choice(len(probs), p=probs)

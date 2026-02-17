import torch
import torch.nn as nn

class CNNDiscriminator(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, num_filters=128):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, num_filters, kernel_size=k)
            for k in (3,5,7)
        ])
        self.fc = nn.Linear(num_filters * len(self.convs), 1)

    def forward(self, x):
        # x: (batch, seq)
        x = self.embed(x).permute(0,2,1)  # (batch, embed, seq)
        feats = [torch.relu(conv(x)).max(dim=2)[0] for conv in self.convs]
        cat = torch.cat(feats, dim=1)
        out = torch.sigmoid(self.fc(cat)).squeeze(-1)
        return out

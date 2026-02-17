import torch
from backend.models.generator import LSTMGenerator
from backend.models.discriminator import CNNDiscriminator
from backend.curriculum.curriculum import get_stage_params
from backend.utils.rdkit_utils import validate_smiles, compute_qed, compute_sa
from backend.dpp.dpp import compute_diversity_reward
import numpy as np


class Trainer:
    def __init__(self, device=None):
        self.device = device or (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
        self.gen = LSTMGenerator(device=self.device)
        self.disc = CNNDiscriminator(self.gen.vocab_size).to(self.device)
        self.opt_g = torch.optim.Adam(self.gen.parameters(), lr=1e-4)
        self.opt_d = torch.optim.Adam(self.disc.parameters(), lr=1e-4)

    def compute_rewards(self, smiles_list, diversity_weight=0.1):
        # compute validity, qed, sa, diversity
        valids = [1.0 if validate_smiles(s) else 0.0 for s in smiles_list]
        qeds = [compute_qed(s) or 0.0 for s in smiles_list]
        sas = [compute_sa(s) or 0.0 for s in smiles_list]
        divs = compute_diversity_reward([s for s in smiles_list if validate_smiles(s)])
        # map back
        div_map = {}
        valid_smiles = [s for s in smiles_list if validate_smiles(s)]
        for s, d in zip(valid_smiles, divs):
            div_map[s] = d
        final_divs = [div_map.get(s, 0.0) for s in smiles_list]
        return np.array(valids), np.array(qeds), np.array(sas), np.array(final_divs)

    def train(self, epochs=60, batch_size=64):
        for epoch in range(1, epochs+1):
            params = get_stage_params(epoch)
            temp = params['temperature']
            div_w = params['diversity_weight']
            # sample from generator
            samples = self.gen.sample_smiles(batch_size, temperature=temp)
            valids, qeds, sas, divs = self.compute_rewards(samples, diversity_weight=div_w)
            # compute reward according to stage
            reward = None
            rcfg = params['reward']
            reward = np.zeros_like(valids, dtype=float)
            if 'validity' in rcfg:
                reward += rcfg['validity'] * valids
            if 'qed' in rcfg:
                reward += rcfg['qed'] * qeds
            if 'sa' in rcfg:
                reward += rcfg['sa'] * sas
            reward += div_w * divs
            # placeholder: apply policy gradient / adversarial update
            # In production implement proper RL/GAN update steps
            print(f"Epoch {epoch}: mean reward {reward.mean():.4f}")

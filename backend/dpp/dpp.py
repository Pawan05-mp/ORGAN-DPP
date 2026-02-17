import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem


def mol_to_fp_array(smiles, radius=2, nbits=2048):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return None
    fp = AllChem.GetMorganFingerprintAsBitVect(m, radius, nBits=nbits)
    arr = np.zeros((nbits,), dtype=np.float32)
    DataStructs = None
    try:
        from rdkit import DataStructs
        DataStructs.ConvertToNumpyArray(fp, arr)
    except Exception:
        # fallback manual
        for i in fp.GetOnBits():
            arr[i] = 1.0
    return arr


def compute_diversity_reward(smiles_list, radius=2, nbits=2048):
    # returns a diversity scalar per molecule based on DPP-like score
    fps = []
    for s in smiles_list:
        fp = mol_to_fp_array(s, radius=radius, nbits=nbits)
        if fp is None:
            fps.append(np.zeros(nbits, dtype=np.float32))
        else:
            fps.append(fp)
    X = np.stack(fps, axis=0).astype(np.float64)
    # normalize
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    Xn = X / norms
    # Gram matrix
    K = np.dot(Xn, Xn.T)
    # add small jitter
    K += np.eye(K.shape[0]) * 1e-6
    # diversity score: logdet of principal minor excluding molecule i? here use diagonal of K
    # compute log-det of full Gram as global diversity then compute per-molecule marginal
    try:
        s, ld = np.linalg.slogdet(K)
        global_ld = ld if s > 0 else 0.0
    except Exception:
        global_ld = 0.0
    # simple per-molecule score: 1 - mean similarity to others
    sims = K
    per = 1.0 - sims.mean(axis=1)
    return per.tolist()


def select_k_diverse(smiles_list, k=10, radius=2, nbits=2048):
    # greedy selection maximizing determinant incrementally (works up to moderate n)
    fps = []
    for s in smiles_list:
        fp = mol_to_fp_array(s, radius=radius, nbits=nbits)
        fps.append(fp if fp is not None else np.zeros(nbits))
    X = np.stack(fps, axis=0)
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    Xn = X / norms
    K = np.dot(Xn, Xn.T)
    selected = []
    remaining = list(range(len(smiles_list)))
    L = np.zeros((0,0))
    for _ in range(min(k, len(remaining))):
        best = None
        best_val = -np.inf
        for i in remaining:
            cand = selected + [i]
            sub = K[np.ix_(cand, cand)]
            val = np.linalg.slogdet(sub + 1e-6 * np.eye(len(sub)))[1]
            if val > best_val:
                best_val = val
                best = i
        selected.append(best)
        remaining.remove(best)
    return [smiles_list[i] for i in selected]

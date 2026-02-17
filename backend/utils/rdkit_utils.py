try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw
    from rdkit.Chem import QED
except Exception:
    Chem = None
    AllChem = None
    Draw = None
    QED = None

import base64
import io


def validate_smiles(smiles: str) -> bool:
    if Chem is None:
        return False
    m = Chem.MolFromSmiles(smiles)
    return m is not None


def compute_qed(smiles: str):
    if QED is None:
        return None
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return None
    return float(QED.qed(m))


def compute_sa(smiles: str):
    # lightweight SA estimator placeholder (higher -> harder)
    # For production include RDKit sascorer
    try:
        m = Chem.MolFromSmiles(smiles)
        if m is None:
            return None
        # crude heuristic: ring count and heavy atom count
        ra = m.GetRingInfo().NumRings()
        ha = m.GetNumHeavyAtoms()
        score = 4.0 + 0.1 * ra - 0.02 * ha
        return float(max(1.0, min(10.0, score)))
    except Exception:
        return None


def mol_to_svg(smiles: str, size=(300, 300)) -> str:
    if Chem is None or Draw is None:
        return ""
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return ""
    svg = Draw.MolsToGridImage([m], molsPerRow=1, subImgSize=size, useSVG=True)
    if hasattr(svg, 'replace'):
        return svg
    return str(svg)

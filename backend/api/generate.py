from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from backend.models.generator import LSTMGenerator
from backend.utils.rdkit_utils import validate_smiles, compute_qed, compute_sa, mol_to_svg
from backend.dpp.dpp import compute_diversity_reward, select_k_diverse
import asyncio

router = APIRouter()


class GenerateRequest(BaseModel):
    batch_size: int = 64
    diversity_weight: float = 0.1
    temperature: float = 1.0
    curriculum_stage: int = 1


class MoleculeOut(BaseModel):
    smiles: str
    qed: Optional[float]
    sa: Optional[float]
    diversity: Optional[float]
    validity: bool


# lightweight singleton generator (would load weights in prod)
GEN = LSTMGenerator()


@router.post("/generate")
async def generate(req: GenerateRequest):
    if req.batch_size < 1 or req.batch_size > 512:
        raise HTTPException(status_code=400, detail="batch_size must be 1..512")

    samples = GEN.sample_smiles(req.batch_size, temperature=req.temperature)

    results = []
    fp_list = []
    for s in samples:
        valid = validate_smiles(s)
        qed = compute_qed(s) if valid else None
        sa = compute_sa(s) if valid else None
        results.append({
            "smiles": s,
            "qed": qed,
            "sa": sa,
            "validity": valid,
            "diversity": None,
        })
        if valid:
            fp_list.append(s)

    # compute diversity rewards via DPP on valid molecules
    if fp_list:
        diversity_scores = compute_diversity_reward(fp_list)
        # assign diversity back to results (match by smiles)
        map_div = {s: d for s, d in zip(fp_list, diversity_scores)}
        for r in results:
            if r["smiles"] in map_div:
                r["diversity"] = map_div[r["smiles"]]

    summary = {"count": len(results), "valid": sum(1 for r in results if r["validity"]) }
    run_id = str(uuid4())

    # In production we'd store run and molecules asynchronously in DB

    return {"run_id": run_id, "molecules": results, "summary_metrics": summary}


@router.get("/metrics/{run_id}")
async def get_metrics(run_id: str):
    # placeholder: real implementation would query DB
    return {"run_id": run_id, "metrics": {}}


@router.get("/download/{run_id}")
async def download_run(run_id: str):
    # placeholder
    return {"run_id": run_id, "url": None}


@router.post("/train")
async def train(background_tasks: BackgroundTasks):
    # enqueue training in background
    background_tasks.add_task(_train_task)
    return {"status": "training_enqueued"}


def _train_task():
    # minimal placeholder; real trainer runs full curriculum
    import time
    time.sleep(1)
    print("Training run finished (placeholder)")

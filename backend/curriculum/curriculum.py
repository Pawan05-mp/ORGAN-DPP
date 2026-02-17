from typing import Dict


def get_stage_params(epoch: int) -> Dict:
    # stages: 1: 1-20, 2:21-40, 3:41-60
    if epoch <= 20:
        return {
            "reward": {"validity": 1.0},
            "temperature": 1.5,
            "diversity_weight": 0.05,
        }
    elif epoch <= 40:
        return {
            "reward": {"validity": 0.5, "qed": 0.5},
            "temperature": 1.0,
            "diversity_weight": 0.10,
        }
    else:
        return {
            "reward": {"validity": 0.3, "qed": 0.3, "sa": 0.4},
            "temperature": 0.7,
            "diversity_weight": 0.15,
        }

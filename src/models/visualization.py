"""Model visualization utilities."""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)


def plot_feature_importance(model_path: str, output_path: str,
                            top_n: int = 20) -> None:
    """Plot feature importance from saved model."""
    try:
        import matplotlib.pyplot as plt

        with open(model_path, "rb") as f:
            data = pickle.load(f)

        model = data["model"]
        importances = model.feature_importances_
        names = [f"feature_{i}" for i in range(len(importances))]

        # Sort by importance
        indices = np.argsort(importances)[-top_n:]

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(len(indices)), importances[indices])
        ax.set_yticks(range(len(indices)))
        ax.set_yticklabels([names[i] for i in indices])
        ax.set_xlabel("Feature Importance")
        ax.set_title(f"Top {top_n} Feature Importances")
        plt.tight_layout()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved feature importance plot to {output_path}")

    except ImportError:
        logger.warning("matplotlib not available, skipping plot")


def plot_roc_curve(y_true: np.ndarray, y_proba: np.ndarray,
                   output_path: Optional[str] = None) -> None:
    """Plot ROC curve."""
    try:
        import matplotlib.pyplot as plt
        from sklearn.metrics import roc_curve, auc

        fpr, tpr, _ = roc_curve(y_true, y_proba)
        roc_auc = auc(fpr, tpr)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend()
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    except ImportError:
        pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        plot_feature_importance(sys.argv[1], sys.argv[2])

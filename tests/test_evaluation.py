import pytest
import numpy as np
from src.models.evaluate import accuracy_score, classification_report

@pytest.fixture
def sample_predictions():
    return {
        "y_true": np.array([0, 1, 1, 0, 1, 0]),
        "y_pred": np.array([0, 1, 0, 0, 1, 1])
    }

def test_accuracy_score(sample_predictions):
    acc = accuracy_score(sample_predictions["y_true"], sample_predictions["y_pred"])
    assert 0 <= acc <= 1, "❌ La precisión debe estar entre 0 y 1."

def test_classification_report(sample_predictions):
    report = classification_report(sample_predictions["y_true"], sample_predictions["y_pred"], target_names=["Negativo", "Positivo"])
    assert "precision" in report, "❌ El reporte de clasificación no se generó correctamente."
    assert "recall" in report, "❌ El reporte de clasificación no incluye recall."
    assert "f1-score" in report, "❌ El reporte de clasificación no incluye F1-score."

if __name__ == "__main__":
    pytest.main()
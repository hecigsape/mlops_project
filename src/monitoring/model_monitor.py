import mlflow
import os

# 📌 Configuración de MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME = "bert_finetuning"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

if not experiment:
    raise ValueError(f"El experimento '{EXPERIMENT_NAME}' no existe en MLflow.")

# 📌 Obtener el último modelo registrado
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time desc"], max_results=1)
if runs.empty:
    raise ValueError("No se encontraron ejecuciones en MLflow.")

latest_run_id = runs.iloc[0]["run_id"]
val_accuracy = float(runs.iloc[0]["metrics.val_accuracy"])

# 📌 Imprimir la métrica de validación
print(f"📊 Validation Accuracy: {val_accuracy:.4f}")

import tensorflow as tf
import pandas as pd
import os
from transformers import TFBertForSequenceClassification, BertTokenizer
import numpy as np
from sklearn.metrics import accuracy_score, classification_report

# 📌 Configuración
MODEL_PATH = "src/models/checkpoints/bert_finetuned"
DATA_PATH = "data/processed/splits/test.parquet"
BATCH_SIZE = 32

# 📌 Cargar el modelo y el tokenizador
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH)

# 📌 Cargar el conjunto de prueba
df = pd.read_parquet(DATA_PATH)
texts, labels = df["text"].tolist(), df["label"].tolist()

# 📌 Tokenización de los datos
def tokenize_data(texts, max_length=128):
    return tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="tf")

test_tokens = tokenize_data(texts)

# 📌 Realizar predicciones
logits = model.predict(test_tokens)[0]
predictions = np.argmax(logits, axis=1)

# 📌 Calcular métricas
accuracy = accuracy_score(labels, predictions)
report = classification_report(labels, predictions, target_names=["Negativo", "Positivo"])

# 📌 Imprimir resultados
print(f"📊 Precisión en el conjunto de prueba: {accuracy:.4f}")
print(report)

# 📌 Guardar resultado en un archivo
eval_output_path = "src/models/evaluation_results.txt"
with open(eval_output_path, "w") as f:
    f.write(f"Validation Accuracy: {accuracy:.4f}\n")
    f.write(report)

print(f"✅ Resultados guardados en {eval_output_path}")
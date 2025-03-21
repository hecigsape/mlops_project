import tensorflow as tf
import os
import mlflow
import mlflow.tensorflow
from transformers import BertTokenizer, TFBertForSequenceClassification
from tensorflow.keras.optimizers.schedules import PolynomialDecay
import pyarrow.parquet as pq

# 📌 Configuración
DATA_PATH = "data/processed/Software_processed.parquet"
SAVE_PATH = "data/processed/splits/"
SAVE = True  # Bandera para guardar o cargar los datos
BATCH_SIZE = 32
EPOCHS = 3
MLFLOW_TRACKING_URI = "http://localhost:5000"  # Ajustar si se usa un servidor remoto

# 📌 Configurar MLflow
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("bert_finetuning")

# 📌 Cargar el tokenizador de BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize_data(text, label, max_length=128):
    tokens = tokenizer(text.numpy().decode("utf-8"), padding="max_length", truncation=True, max_length=max_length, return_tensors="tf")
    return {key: tf.convert_to_tensor(val.numpy()) for key, val in tokens.items()}, label

def load_dataset(file_path, batch_size=32, shuffle=True):
    table = pq.read_table(file_path)
    text_data = table.column("text").to_pylist()
    labels = table.column("label").to_pylist()

    dataset = tf.data.Dataset.from_tensor_slices((text_data, labels))
    dataset = dataset.map(lambda x, y: tf.py_function(tokenize_data, [x, y], [{"input_ids": tf.int32, "attention_mask": tf.int32}, tf.int32]))
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(text_data))
    dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    
    return dataset

# 📌 Cargar datasets
train_dataset = load_dataset("data/processed/splits/train.parquet", batch_size=BATCH_SIZE)
val_dataset = load_dataset("data/processed/splits/val.parquet", batch_size=BATCH_SIZE)
test_dataset = load_dataset("data/processed/splits/test.parquet", batch_size=BATCH_SIZE, shuffle=False)

# 📌 Cargar modelo BERT preentrenado
model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# 📌 Configurar optimizador y pérdida
total_steps = len(train_dataset) * EPOCHS
learning_rate_fn = PolynomialDecay(initial_learning_rate=5e-5, end_learning_rate=0, decay_steps=total_steps)
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate_fn)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])

# 📌 Entrenamiento con MLflow
with mlflow.start_run():
    mlflow.log_params({"batch_size": BATCH_SIZE, "epochs": EPOCHS, "learning_rate": 5e-5})
    history = model.fit(train_dataset, validation_data=val_dataset, epochs=EPOCHS)
    
    # Registrar métricas
    for epoch in range(EPOCHS):
        mlflow.log_metric("train_accuracy", history.history['accuracy'][epoch], step=epoch)
        mlflow.log_metric("val_accuracy", history.history['val_accuracy'][epoch], step=epoch)
    
    # Guardar modelo en MLflow
    mlflow.tensorflow.log_model(model, "bert_finetuned")

# 📌 Guardar el modelo localmente
model.save_pretrained("src/models/checkpoints/bert_finetuned")

print("✅ Entrenamiento finalizado y modelo guardado.")

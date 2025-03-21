import pytest
import pandas as pd
import tensorflow as tf
import os
from src.data.preprocessing import filter_english_reviews, remove_neutral_reviews, clean_text
from src.models.train import tokenize_data
from src.models.evaluate import accuracy_score

@pytest.fixture
def sample_data():
    data = {
        "text": ["I love this product!", "This game is terrible", "Mediocre experience"],
        "language": ["en", "en", "es"],
        "rating": [5, 1, 3]
    }
    return pd.DataFrame(data)

# 📌 Pruebas para Preprocesamiento
def test_filter_english_reviews(sample_data):
    df_filtered = filter_english_reviews(sample_data)
    assert all(df_filtered["language"] == "en"), "❌ No se eliminaron los textos en otros idiomas."

def test_remove_neutral_reviews(sample_data):
    df_filtered = remove_neutral_reviews(sample_data)
    assert all(df_filtered["rating"] != 3), "❌ No se eliminaron correctamente las reseñas neutrales."

def test_clean_text(sample_data):
    df_cleaned = clean_text(sample_data)
    assert not any(df_cleaned["text"].str.contains(r"[^a-zA-Z0-9 ]")), "❌ No se limpiaron los caracteres especiales."

# 📌 Pruebas para Tokenización
def test_tokenize_data():
    texts = ["This is a test", "Another example"]
    labels = [1, 0]
    tokens, labels_tensor = tokenize_data(texts, labels)
    assert isinstance(tokens, dict), "❌ Tokenización incorrecta"
    assert isinstance(labels_tensor, tf.Tensor), "❌ Labels no están en formato TensorFlow."

# 📌 Pruebas para Evaluación
def test_accuracy_score():
    y_true = [0, 1, 1, 0]
    y_pred = [0, 1, 0, 0]
    acc = accuracy_score(y_true, y_pred)
    assert 0 <= acc <= 1, "❌ La precisión debe estar entre 0 y 1."

if __name__ == "__main__":
    pytest.main()

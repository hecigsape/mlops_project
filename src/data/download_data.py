import os
import requests
import shutil
import gzip

def download_and_extract_dataset():
    """
    Descarga y extrae el dataset de Amazon Reviews 2023 - Categoría Software.
    """

    # Definir la URL del archivo y la ruta de destino
    url = "https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/raw/review_categories/Software.jsonl.gz"
    download_path = "data/raw/Software.jsonl.gz"
    extract_path = "data/raw/Software.jsonl"

    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    # Descargar el archivo
    print("📥 Descargando archivo...")
    response = requests.get(url, stream=True)
    with open(download_path, "wb") as file:
        shutil.copyfileobj(response.raw, file)
    print("✅ Descarga completada.")

    # Extraer el archivo .gz
    print("📂 Extrayendo archivo...")
    with gzip.open(download_path, "rb") as f_in:
        with open(extract_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print("✅ Extracción completada.")

    # Opcional: eliminar el archivo comprimido
    os.remove(download_path)
    print("🗑️ Archivo comprimido eliminado.")

if __name__ == "__main__":
    download_and_extract_dataset()

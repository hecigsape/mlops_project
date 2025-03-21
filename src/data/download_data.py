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

    # Descargar el archivo con validación
    print("📥 Descargando archivo...")
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        print(f"❌ Error en la descarga: Código {response.status_code}")
        print(f"🔗 URL de descarga: {url}")
        return

    with open(download_path, "wb") as file:
        shutil.copyfileobj(response.raw, file)
    
    print("✅ Descarga completada.")

    # Verificar si el archivo descargado es realmente un archivo Gzip
    try:
        with gzip.open(download_path, "rb") as f:
            f.read(1)  # Intenta leer un byte para comprobar si es un archivo válido
    except Exception as e:
        print(f"❌ Error: El archivo no es un Gzip válido. {str(e)}")
        print("⚠️ Verifica la URL de descarga o intenta descargar manualmente.")
        return

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

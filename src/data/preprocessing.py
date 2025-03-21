from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, lower, regexp_replace, count, when
from pyspark.sql.window import Window
import fasttext
from pyspark.sql.types import StringType
import os 
from pyspark.sql import functions as F

file_path_model = "data/models/lid.176.bin"

def create_spark_session():
    """Crea una sesión de Spark."""
    return SparkSession.builder.appName("PreprocesamientoAmazonReviews").getOrCreate()

def load_data(file_path, spark):
    """Carga los datos desde Parquet."""
    print(f"📥 Cargando datos desde {file_path}...")
    df = spark.read.parquet(file_path)
    print("✅ Datos cargados correctamente.")
    return df

def filter_english_reviews(df):
    """Filtra solo las reseñas en inglés si la columna 'language' existe."""
    if "language" in df.columns:
        print("\n🗑️ Eliminando reseñas en idiomas distintos al inglés...")
        # df = df.filter(col("language") == "en")
        # df = df.repartition("language").filter(col("language") == "en")
        # df = df.select("language", "text").filter(col("language") == "en")
        df = df.filter(col("language") == "en").select("language", "label","text")

        print(f"✅ Total de registros después del filtro de idioma: {df.count()}")
    else:
        print("\n⚠️ Advertencia: La columna 'language' no existe en el DataFrame. No se aplica el filtro.")
    
    return df

def remove_neutral_reviews(df):
    """Elimina reseñas de 3 estrellas para convertirlo en un problema binario."""
    print("\n🗑️ Eliminando reseñas de 3 estrellas...")
    df = df.filter(col("rating") != 3)
    
    # Convertir ratings en clasificación binaria (0 = negativo, 1 = positivo)
    df = df.withColumn("label", when(col("rating") <= 2, 0).otherwise(1))
    
    print(f"✅ Total de registros después de eliminación de neutrales: {df.count()}")
    return df

def clean_text(df):
    """Limpia el texto de las reseñas eliminando caracteres especiales."""
    print("\n🧹 Limpiando texto...")
    df = df.withColumn("text", lower(col("text")))  # Convertir a minúsculas
    df = df.withColumn("text", regexp_replace(col("text"), "[^a-zA-Z0-9\s]", ""))  # Eliminar caracteres especiales
    df = df.withColumn("text", regexp_replace(col("text"), "\s+", " "))  # Eliminar espacios extras
    print("✅ Texto limpiado.")
    return df

def remove_duplicates_and_empty(df):
    """Elimina duplicados y valores nulos."""
    print("\n🗑️ Eliminando valores nulos y duplicados...")
    # df = df.filter((col("text").isNotNull()) & (col("text") != ""))  # Eliminar reseñas vacías
    # df = df.dropDuplicates(["text"])  # Eliminar reseñas duplicadas
    df = df.filter((col("text").isNotNull()) & (col("text") != "")).dropDuplicates(["text"])

    # print(f"✅ Total de registros después de limpieza: {df.count()}")
    return df

def undersampling(df):
    """Balancea las clases reduciendo la cantidad de reseñas positivas (Undersampling)."""
    print("\n⚖️ Aplicando Undersampling para balancear clases...")

    # Contar cantidad de positivos y negativos
    """class_counts = df.groupBy("label").count().collect()
    positive_count = next(x["count"] for x in class_counts if x["label"] == 1)
    negative_count = next(x["count"] for x in class_counts if x["label"] == 0)
    min_class_count = min(positive_count, negative_count)  # Seleccionar la menor cantidad
    """
    # ✅ Contar clases de forma más eficiente sin `collect()`
    class_counts = df.groupBy("label").count().toPandas().set_index("label")["count"]
    positive_count, negative_count = class_counts.get(1, 0), class_counts.get(0, 0)
    min_class_count = min(positive_count, negative_count)

    print(f"🔹 Positivos: {positive_count}, Negativos: {negative_count}")
    print(f"✅ Reduciéndolos a: {min_class_count}")

    """# Seleccionar aleatoriamente `min_class_count` reseñas de cada clase
    df_positive = df.filter(col("label") == 1).sample(False, min_class_count / positive_count, seed=42)
    df_negative = df.filter(col("label") == 0).sample(False, min_class_count / negative_count, seed=42)

    df_balanced = df_positive.union(df_negative)
    """
    # ✅ Filtrar y muestrear en una sola operación
    df_balanced = (
        df.withColumn("rand", F.rand(seed=42))  # Agregar una columna aleatoria para el muestreo
        .withColumn("rank", F.row_number().over(Window.partitionBy("label").orderBy("rand")))
        .filter(col("rank") <= min_class_count)  # Filtrar para balancear
        .drop("rand", "rank")  # Limpiar columnas auxiliares
    )

    print(f"✅ Total de registros después del balanceo: {df_balanced.count()}")
    return df_balanced

def save_cleaned_data(df, output_path):
    """Guarda los datos procesados en Parquet."""
    print(f"\n💾 Guardando datos procesados en {output_path}...")
    df.write.mode("overwrite").parquet(output_path)
    print("✅ Datos guardados correctamente.")

# Función para cargar el modelo FastText en cada worker de Spark
def get_fasttext_model():
    """Carga el modelo FastText en cada worker solo una vez."""
    return fasttext.load_model("models/lid.176.bin")

def detect_language(text):
    """Detecta el idioma usando FastText."""
    try:
        if not text:
            return "unknown"

        # Cargar modelo FastText en cada worker
        model = get_fasttext_model()

        label = model.predict([text.replace("\n", " ")])
        return label[0][0][0].replace("__label__", "")
    except Exception:
        return "unknown"

def check_and_download_file(file_path, url):
    """
    Verifica si el archivo existe en la ruta especificada.
    Si no existe, lo descarga usando wget.

    """
    if os.path.exists(file_path):
        print(f"✅ El archivo ya existe: {file_path}")
    else:
        print(f"⚠️ El archivo no existe. Descargando desde: {url}")
        os.system(f"wget {url} -P {os.path.dirname(file_path)}")
        print("✅ Descarga completada.")

    
detect_language_udf = udf(detect_language, StringType())

def add_language_column(df):
    # Convertir la función en UDF para PySpark

    """Añade la columna 'language' con la detección de idioma."""
    print("\n🌍 Detectando idioma de las reseñas...")
    df = df.withColumn("language", detect_language_udf(col("text")))
    print("✅ Detección de idioma completada.")
    return df
def check_and_download_file(file_path, url):
    """
    Verifica si el archivo existe en la ruta especificada.
    Si no existe, lo descarga usando wget.

    """
    if os.path.exists(file_path):
        print(f"✅ El archivo ya existe: {file_path}")
    else:
        print(f"⚠️ El archivo no existe. Descargando desde: {url}")
        os.system(f"wget {url} -P {os.path.dirname(file_path)}")
        print("✅ Descarga completada.")


def detect_language_udf():
    model = None  # Variable para almacenar el modelo en caché

    def detect_language(text):
        nonlocal model
        if model is None:
            model = fasttext.load_model(file_path_model)  # ✅ Carga del modelo en cada worker
        try:
            if not text:
                return "unknown"
            label = model.predict([text.replace("\n", " ")])
            return label[0][0][0].replace("__label__", "")
        except Exception:
            return "unknown"

    return detect_language






if __name__ == "__main__":
    # 📌 Definir rutas
    interim_data_path = "data/interim/Software_interim.parquet"
    processed_data_path = "data/processed/Software_processed.parquet"

    # Crear sesión de Spark
    spark = create_spark_session()

    # Cargar datos
    df = load_data(interim_data_path, spark)
    
    #Verifica si el archivo existe en la ruta especificada.   
    url = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
    check_and_download_file(file_path_model, url)
    
    # Aplicar detección de idioma
    df = add_language_column(df)

    # 📌 Verificar los datos antes de seguir
    df.select("text", "language").show(5, truncate=False)

    # Eliminar reseñas neutrales y convertir a clasificación binaria
    df = filter_english_reviews(df)
    df = remove_neutral_reviews(df)

    # Preprocesar datos
    df = clean_text(df)
    df = remove_duplicates_and_empty(df)

    # Aplicar Undersampling
    df = undersampling(df)

    # Guardar datos procesados
    save_cleaned_data(df, processed_data_path)

    print("\n🎯 Proceso de preprocesamiento completado.")
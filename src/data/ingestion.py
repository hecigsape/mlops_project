from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

def create_spark_session():
    """
    Crea una sesión de Spark.
    """
    return SparkSession.builder.appName("AmazonSoftwareReviews").getOrCreate()

def load_jsonl(file_path, spark):
    """
    Carga el dataset JSONL en un DataFrame de Spark.
    """
    print(f"📥 Cargando datos desde {file_path}...")
    df = spark.read.json(file_path)
    print("✅ Datos cargados correctamente.")
    return df

def explore_data(df):
    """
    Explora la estructura y contenido del dataset.
    """
    print("\n📌 Esquema del dataset:")
    df.printSchema()
    
    print("\n📊 Cantidad total de registros:")
    print(f"✅ Total de registros: {df.count()}")
    
    print("\n🔎 Verificación de valores nulos:")
    df.select([count(col(c)).alias(c) for c in df.columns]).show()

def save_as_parquet(df, output_path):
    """
    Guarda el DataFrame en formato Parquet para mayor eficiencia.
    """
    print(f"\n💾 Guardando datos en {output_path}...")
    df.write.mode("overwrite").parquet(output_path)
    print("✅ Datos guardados correctamente.")

if __name__ == "__main__":
    # 📌 Definir rutas
    raw_data_path = "data/raw/Software.jsonl"
    interim_data_path = "data/interim/Software_interim.parquet"

    # Crear sesión de Spark
    spark = create_spark_session()

    #  Cargar datos
    df = load_jsonl(raw_data_path, spark)

    #  Explorar los datos
    explore_data(df)

    # Guardar en Parquet
    save_as_parquet(df, interim_data_path)

    # Finalización
    print("\n🎯 Proceso de ingestion completado.")

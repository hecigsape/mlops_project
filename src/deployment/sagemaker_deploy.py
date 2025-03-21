import boto3
import sagemaker
from sagemaker.model import Model
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer
import os

# 📌 Configuración de AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_URL = os.getenv("S3_BUCKET_URL")
MODEL_NAME = "bert-finetuned-nlp"
ENDPOINT_NAME = "bert-nlp-endpoint"
INSTANCE_TYPE = "ml.m5.large"
ROLE_ARN = os.getenv("AWS_SAGEMAKER_ROLE")  # ARN del rol con permisos para SageMaker

# 📌 Inicializar clientes de AWS
sagemaker_client = boto3.client("sagemaker", region_name=AWS_REGION)
s3_client = boto3.client("s3", region_name=AWS_REGION)

# 📌 Descargar el modelo desde S3
model_path = f"{S3_BUCKET_URL}/bert_finetuned/model.tar.gz"
print(f"📥 Descargando modelo desde {model_path}...")
local_model_path = "/tmp/model.tar.gz"
s3_client.download_file(S3_BUCKET_URL.replace("s3://", ""), "bert_finetuned/model.tar.gz", local_model_path)
print("✅ Modelo descargado correctamente.")

# 📌 Crear el objeto modelo en SageMaker
model = Model(
    image_uri=sagemaker.image_uris.retrieve("huggingface", AWS_REGION, "transformers-tensorflow-cpu"),
    model_data=model_path,
    role=ROLE_ARN,
    predictor_cls=Predictor,
    serializer=JSONSerializer(),
    deserializer=JSONDeserializer()
)

# 📌 Desplegar el modelo en SageMaker
print("🚀 Desplegando el modelo en SageMaker...")
predictor = model.deploy(
    initial_instance_count=1,
    instance_type=INSTANCE_TYPE,
    endpoint_name=ENDPOINT_NAME
)
print(f"✅ Modelo desplegado en SageMaker en el endpoint: {ENDPOINT_NAME}")

# 📌 Prueba de Inferencia
test_data = {"inputs": "This product is amazing!"}
response = predictor.predict(test_data)
print(f"📝 Respuesta del modelo: {response}")
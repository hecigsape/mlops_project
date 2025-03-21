import pytest
import boto3
import os
from botocore.exceptions import NoCredentialsError

# 📌 Configuración de AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT_NAME = os.getenv("SAGEMAKER_ENDPOINT_NAME", "bert-nlp-endpoint")
sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=AWS_REGION)

def test_sagemaker_endpoint_exists():
    """Verifica que el endpoint de SageMaker existe."""
    sagemaker_client = boto3.client("sagemaker", region_name=AWS_REGION)
    try:
        response = sagemaker_client.describe_endpoint(EndpointName=ENDPOINT_NAME)
        assert response["EndpointStatus"] in ["InService", "Creating"], "❌ El endpoint no está activo."
    except sagemaker_client.exceptions.ClientError:
        pytest.fail("❌ El endpoint de SageMaker no existe.")


def test_sagemaker_inference():
    """Prueba una inferencia en el endpoint de SageMaker."""
    test_data = {"inputs": "This product is amazing!"}
    try:
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=str(test_data)
        )
        result = response["Body"].read().decode("utf-8")
        assert result is not None, "❌ No se recibió respuesta del modelo."
    except NoCredentialsError:
        pytest.fail("❌ No se encontraron credenciales de AWS.")
    except Exception as e:
        pytest.fail(f"❌ Error en la inferencia: {str(e)}")

if __name__ == "__main__":
    pytest.main()

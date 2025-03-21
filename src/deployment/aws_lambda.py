import json
import boto3
import os

# 📌 Configuración de AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT_NAME = os.getenv("SAGEMAKER_ENDPOINT_NAME", "bert-nlp-endpoint")
sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=AWS_REGION)

def lambda_handler(event, context):
    """Función Lambda para invocar el endpoint de SageMaker y realizar inferencias."""
    try:
        body = json.loads(event["body"])
        input_data = {"inputs": body["text"]}

        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps(input_data)
        )

        result = json.loads(response["Body"].read().decode("utf-8"))
        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": result})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
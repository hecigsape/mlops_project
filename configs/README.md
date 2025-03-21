# ⚙️ Configuración del Proyecto

Este directorio contiene los archivos de configuración para la ejecución y despliegue del modelo.

## 📂 Estructura de la Carpeta `configs/`

```
configs/
├── config.yaml         # Configuración general del proyecto
├── logging.yaml        # Configuración del sistema de logs
├── model_params.yaml   # Hiperparámetros del modelo
├── aws_config.json     # Configuración de AWS para despliegue en SageMaker
```

## 📌 Descripción de Archivos

### 🔹 `config.yaml` (Configuración General)
- Define rutas de datos, modelos y directorios de trabajo.
- Contiene parámetros para entrenamiento y despliegue.
- Configura umbrales para monitoreo del modelo.

### 🔹 `logging.yaml` (Configuración de Logs)
- Define formatos y niveles de logs (DEBUG, INFO, ERROR).
- Especifica dónde se guardarán los logs (`logs/mlops_pipeline.log`).
- Permite monitorear eventos clave en preprocesamiento, entrenamiento y despliegue.

### 🔹 `model_params.yaml` (Hiperparámetros del Modelo)
- Contiene la arquitectura del modelo (`bert-base-uncased`).
- Define `batch_size`, `learning_rate`, `dropout`, `epochs`, etc.
- Configura parámetros de optimización (`adamw`, `weight_decay`).

### 🔹 `aws_config.json` (Configuración de AWS)
- Define la región (`us-east-1`) y el bucket S3 para almacenamiento.
- Incluye el ARN del rol de SageMaker para permisos.
- Contiene credenciales de AWS (se recomienda almacenar en `secrets`).

## 🚀 Cómo Usar estos Archivos
1️⃣ **Editar `config.yaml` para cambiar rutas o hiperparámetros.**
2️⃣ **Modificar `logging.yaml` si se necesita más detalle en los logs.**
3️⃣ **Actualizar `aws_config.json` con las credenciales correctas antes del despliegue.**

---
📢 **Estos archivos permiten gestionar la configuración de manera centralizada para facilitar la reproducibilidad del proyecto.**
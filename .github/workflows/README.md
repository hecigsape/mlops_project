# 🚀 Automatización con GitHub Actions

Este directorio contiene los archivos de configuración de **GitHub Actions** para la integración y despliegue continuo del proyecto.

## 📂 Estructura de la Carpeta `.github/workflows/`

```
.github/workflows/
├── ci.yml           # Integración Continua (linting, pruebas unitarias, cobertura)
├── cd.yml           # Despliegue del modelo en AWS SageMaker
├── monitoring.yml   # Monitoreo del modelo y detección de data drift
```

## 🛠️ Descripción de los Workflows

### 🔹 `ci.yml` (Integración Continua)
- Ejecuta **Flake8** para verificar el estilo de código.
- Corre **pytest** para ejecutar pruebas unitarias.
- Genera un **reporte de cobertura de código**.
- Se activa en **cada push a `dev` y en PRs a `main`**.

### 🔹 `cd.yml` (Despliegue Continuo)
- Ejecuta el **preprocesamiento y entrenamiento del modelo**.
- Evalúa la precisión del modelo antes de desplegarlo.
- Sube el modelo a **AWS S3**.
- Si supera el umbral de calidad, **despliega en AWS SageMaker**.
- Se ejecuta en **cada push a `main` y automáticamente cada lunes**.

### 🔹 `monitoring.yml` (Monitoreo del Modelo)
- Consulta **MLflow** para monitorear `val_accuracy`.
- Si la precisión baja **por debajo del 85%**, activa una alerta.
- Puede enviar un **correo de alerta** y activar el reentrenamiento.
- Se ejecuta **diariamente a las 6 AM UTC**.

## 🚀 Cómo Ver los Workflows en GitHub
1️⃣ Ir a **GitHub → Repositorio → Actions**.
2️⃣ Seleccionar el workflow (`CI`, `CD`, `Monitoring`).
3️⃣ Revisar los logs de ejecución.

## 📌 Notas
- Antes de ejecutar `cd.yml`, asegúrate de que los **secretos de AWS** están configurados en GitHub.
- Si `monitoring.yml` falla, revisa las métricas en MLflow antes de forzar un reentrenamiento.

---
📢 **Estos workflows garantizan que el modelo siempre esté actualizado y funcionando correctamente en producción.**

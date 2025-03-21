# 🧪 Pruebas Unitarias del Proyecto

Este directorio contiene las pruebas unitarias para validar el correcto funcionamiento de los módulos clave del proyecto.

## 📂 Estructura de la Carpeta `tests/`

```
tests/
├── test_preprocessing.py   # Pruebas para el preprocesamiento de datos
├── test_training.py        # Pruebas para el entrenamiento del modelo
├── test_evaluation.py      # Pruebas para la evaluación del modelo
├── test_deployment.py      # Pruebas para el despliegue en AWS SageMaker
```

## 🚀 Cómo Ejecutar las Pruebas

1️⃣ **Instalar las dependencias:**
```bash
pip install -r requirements.txt
```

2️⃣ **Ejecutar todas las pruebas:**
```bash
pytest tests/
```

3️⃣ **Ejecutar pruebas específicas:**
```bash
pytest tests/test_preprocessing.py
pytest tests/test_training.py
pytest tests/test_evaluation.py
pytest tests/test_deployment.py
```

## ✅ Descripción de Cada Archivo

- **`test_preprocessing.py`** → Valida que los datos sean limpiados correctamente.
- **`test_training.py`** → Verifica que la tokenización y el entrenamiento del modelo sean correctos.
- **`test_evaluation.py`** → Evalúa la precisión del modelo y genera reportes.
- **`test_deployment.py`** → Comprueba que el modelo esté correctamente desplegado en AWS SageMaker y pueda realizar inferencias.

## 📌 Notas
- Antes de correr `test_deployment.py`, asegúrate de que el endpoint de SageMaker está activo.
- Las pruebas deben pasar antes de hacer `merge` a `main` en GitHub Actions.

---

📢 **Si encuentras errores en las pruebas, revisa los logs y ajusta el código antes de desplegar.**
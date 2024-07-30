# basic_GCP_ML_project
Este repositorio muestra un ejemplo de un flujo de trabajo de machine learning utilizando Google Cloud Platform (GCP).  El proyecto incluye la extracción y transformación de datos,entrenamiento y despliegue de un modelo de Regresión Logistica para calculuar la probabilidad de incumplimiento de una cartera de clientes con préstamos personales. 
Finalmente se realiza una ejecución del modelo para hacer predicciones en modo batch.

# Descripción de archivos:

### `scripts/extract_and_transform.py`

Este script extrae y transforma datos desde BigQuery. Los datos transformados se almacenan en una tabla de BigQuery para su uso posterior.

### `scripts/train_and_deploy.py`

Este script entrena un modelo de machine learning utilizando los datos transformados. Luego, el modelo entrenado se despliega en AI Platform para predicciones futuras.

### `scripts/make_batch_predictions.py`

Este script realiza predicciones en batch utilizando el modelo desplegado en AI Platform. Los resultados de las predicciones se descargan desde Google Cloud Storage.

### `notebooks/etl_and_model_training.ipynb`

Un notebook interactivo que muestra el flujo completo del proceso ETL y el entrenamiento del modelo en un formato visual.

## Requisitos

Asegúrate de tener las siguientes librerías instaladas y credenciales necesarias para:

pandas

scikit-learn

google-cloud-bigquery

google-cloud-storage

joblib


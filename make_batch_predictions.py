from google.cloud import bigquery
import pandas as pd
from google.cloud import storage
import subprocess

# Configurar el cliente de BigQuery
client = bigquery.Client()

# Definir la consulta SQL para extraer los datos de predicción
prediction_query = """
    SELECT 
        ID_CREDITO,
        ANTIGUEDAD_CLIENTE,
        FRECUENCIA_DE_PAGO,
        CUOTAS_PAGADAS,
        DIAS_MORA,
        BC_SCORE,
        FICO_SCORE,
        CAPACIDAD_DE_PAGO_ESTIMADA,
        PROMEDIO_BEHAVIOR_SCORE,
        NUMERO_CREDITOS_ANTERIORES,
        NUM_CONSULTAS_6M_BC,
        MAX_MOP_BC,
        MAX_MOP_CC,
        NUM_CUENTAS_ABUERTAS_6M,
        MAX_MORA_BC,
        MAX_MORA_CC
    FROM 
        `RISK_ANALITYCS.CARTERA.COSECHAS`
    WHERE 
        ID_PRODUCTO=106 AND FLAG='VALIDATION' AND
        FECHA_REPORTE BETWEEN '2022-01-31' AND '2024-01-31' AND
        FLAG_CASTIGO=0
"""

# Ejecutar la consulta y almacenar los resultados en un DataFrame de pandas
df_prediction = client.query(prediction_query).to_dataframe()

# Aquí se puede realizar la predicción directamente usando el modelo ya entrenado en AI Platform
# Para este ejemplo, se asume que el modelo está en AI Platform y se utiliza un job de predicción en batch

# Subir el DataFrame directamente a Google Cloud Storage en formato CSV sin guardar localmente
bucket_name = 'RISK_MODELS'
output_file = 'prediction_data.csv'
df_prediction.to_csv(f'gs://{bucket_name}/{output_file}', index=False)


# Ejecutar un job de predicción en batch en AI Platform
job_name = f'prediction_job_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}'
subprocess.run([
    'gcloud', 'ai-platform', 'jobs', 'submit', 'prediction', job_name,
    '--model', 'logistic_regression_model',
    '--version', 'v1',
    '--data-format', 'TEXT',
    '--input-paths', f'gs://{bucket_name}/{output_file}',
    '--output-path', f'gs://{bucket_name}/prediction_results/',
    '--region', 'us-central1'
])

# Descargar los resultados de las predicciones desde Cloud Storage
result_blob = f'gs://{bucket_name}/prediction_results/prediction.results-00000-of-00001'
result_blob.download_to_filename('predictions.csv')

# Leer los resultados en un DataFrame
predictions = pd.read_csv('predictions.csv')
print(predictions.head())

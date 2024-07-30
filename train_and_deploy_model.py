from google.cloud import bigquery
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
from google.cloud import storage
import subprocess

# Configurar el cliente de BigQuery
client = bigquery.Client()

# Leer los datos transformados desde la tabla en storage de BigQuery
query = """
    SELECT * FROM `RISK_ANALITYCS.CARTERA.clasificacion_clientes`
"""
df_transformed = client.query(query).to_dataframe()

# Dividir los datos en conjuntos de entrenamiento y prueba
X = df_transformed.drop(columns=['TARGET'])
y = df_transformed['TARGET']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo de regresión logística
model = LogisticRegression()
model.fit(X_train, y_train)

# Hacer predicciones y evaluar el modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy:.2f}")

# Guardar el modelo en un archivo
joblib.dump(model, 'logistic_regression_model.pkl')

# Subir el modelo a Google Cloud Storage
storage_client = storage.Client()
bucket_name = 'RISK_MODELS' 
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob('logistic_regression_model.pkl')
blob.upload_from_filename('logistic_regression_model.pkl')


# Crear un modelo en AI Platform
subprocess.run([
    'gcloud', 'ai-platform', 'models', 'create', 'logistic_regression_model', '--regions', 'us-central1'
])

# Crear una versión del modelo
subprocess.run([
    'gcloud', 'ai-platform', 'versions', 'create', 'v1', '--model', 'logistic_regression_model',
    '--origin', f'gs://{bucket_name}/logistic_regression_model.pkl', '--runtime-version', '2.3',
    '--python-version', '3.7', '--framework', 'SCIKIT_LEARN'
])

from google.cloud import bigquery

# Configuraración del cliente de BigQuery
client = bigquery.Client()

# Consulta SQL para extraer y transformar los datos
query = """
    CREATE OR REPLACE TABLE  `RISK_ANALITYCS.CARTERA.clasificacion_clientes` AS 
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
        MAX_MORA_CC,
        CASE 
            WHEN MOROSO = 'SI' THEN 1
            WHEN CREDITO_MOROSO = 'NO' THEN 0
            ELSE -1
        END AS TARGET
    FROM 
        `RISK_ANALITYCS.CARTERA.COSECHAS`
    WHERE 
        ID_PRODUCTO=106 AND FLAG='TRAIN' AND
        FECHA_REPORTE BETWEEN 20220131 AND 20240131 AND
        FLAG_CASTIGO=0
"""

# Ejecutar la consulta
client.query(query).result()
print("Datos extraídos y transformados, y almacenados en BigQuery.")

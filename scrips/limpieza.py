import pandas as pd 
import os 
import shutil
import logging
from datetime import datetime


os.makedirs('logs', exist_ok=True)# lo que  hacemos verifica si existe la carpeta logs si no la crea 




logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/limpieza.log"),
        logging.StreamHandler()
    ]
)
def cargar_datos(ruta):
    logging.info("Cargando dataset...")
    df = pd.read_csv(ruta)
    logging.info(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def id_nulo(df):
    logging.info("eliminando id nulos")
    
    df=df.dropna(subset=['id_mascota'])

    return df
    #se eencarga de eliminar los id nulos con el comando dropna y el subset indica que se fije en la columna id para eliminar las filas que tengan id nulo


def precio_consulta(df):
    logging.info("aplicando descuento del 10% precio mayor a 10000")
    df.loc[df['costo_consulta'] > 100, 'costo_consulta'] *= 0.9
    logging.info("descuento aplicado correctamente")
    return df 
    #aplica un descuento del 10% a las consultas que tengan un precio mayor a 10000

def limpiar_datos(df):
    total_inicial = len(df)
    logging.info("Iniciando limpieza...")

    # 1. Eliminar fila completamente vacía (id=6)
    df = df.dropna(how='all')

    # 2. Eliminar filas sin nombre (id=33 — sin nombre no se puede identificar la mascota)
    df = df.dropna(subset=['nombre'])

    # 3. Estandarizar especie y nombre ANTES de buscar duplicados reales
    df['especie'] = df['especie'].str.lower().str.strip()
    df['especie'] = df['especie'].replace({'perra': 'perro', 'gata': 'gato', 'cat': 'gato'})
    df['nombre'] = df['nombre'].str.strip().str.title()

    # 4. Eliminar duplicados exactos: mismo nombre + dueño + fecha + motivo
    #    (el caso Firulais: misma visita duplicada)
    df = df.drop_duplicates(subset=['nombre', 'dueño_nombre', 'fecha_consulta', 'motivo_consulta'], keep='first')

    logging.info(f"Registros eliminados en limpieza: {total_inicial - len(df)}")
    return df

def transformar_datos(df):
    logging.info("Aplicando transformaciones...")

    # 1. Estandarizar fechas (maneja formatos mezclados como 2023-03-15, 15/04/2023 y 20230601)
    df['fecha_consulta'] = pd.to_datetime(df['fecha_consulta'], dayfirst=True, errors='coerce', format='mixed')

    # 2. Eliminar outliers de peso imposibles (Rex y Garfield con 350kg y 9999kg)
    df = df[df['peso_kg'] <= 120]

    # 3. Eliminar edades negativas (Fido con edad -1)
    df = df[df['edad_años'].isna() | (df['edad_años'] >= 0)]

    # 4. Estandarizar texto
    df['raza'] = df['raza'].str.strip().str.title()
    df['dueño_nombre'] = df['dueño_nombre'].str.strip().str.title()

    # 5. Columna derivada: rango de edad
    def clasificar_edad(edad):
        if pd.isna(edad):   return 'desconocido'
        elif edad <= 2:     return 'cachorro'
        elif edad <= 8:     return 'adulto'
        else:               return 'senior'

    df['rango_edad'] = df['edad_años'].apply(clasificar_edad)

    logging.info("Transformaciones aplicadas correctamente")
    return df

def guardar_datos(df, ruta_salida):
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df.to_csv(ruta_salida, index=False)
    logging.info(f"Archivo guardado en {ruta_salida} con {len(df)} registros")

# ─── EJECUCIÓN PRINCIPAL ────────────────────────────────

def main():
    df = cargar_datos('data/raw/mascotas.csv')
    df = limpiar_datos(df)
    df = transformar_datos(df)
    df = id_nulo(df)
    df = precio_consulta(df)
    guardar_datos(df, 'data/processed/mascotas_limpio.csv')
    logging.info("Pipeline finalizado correctamente ✓")

if __name__ == "__main__":
    main()


# src/datos/EDA.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
from pathlib import Path

from src.configuraciones.config_params import conf

## Definimos la CLASE EDA
## input_path: ruta del archivo CSV de entrada.
## output_path: ruta donde se guardará el CSV limpio.
## skew_threshold: define un umbral para decidir si se usa la media o la mediana al imputar datos faltantes.
## self.df: contendrá el DataFrame cargado

class EDA:
    
    def __init__(self, input_path: Union[Path, pd.DataFrame, None], output_path: Optional[Path], skew_threshold: float):
        """input_path puede ser:
        - Path: ruta a un CSV que se leerá cuando se llame a load_dataset()
        - pd.DataFrame: un DataFrame ya cargado (se usará directamente)
        - None: permite crear el objeto y asignar `df` manualmente antes de ejecutar los pasos

        output_path puede ser None si se quiere trabajar en memoria y no guardar el CSV.
        """
        self.input_path = input_path            # Ruta del dataset original o DataFrame
        self.output_path = output_path          # Ruta de salida del dataset limpio (o None)
        self.skew_threshold = skew_threshold    # Umbral de asimetría para decidir método de imputación
        self.df = None                          # DataFrame que contendrá los datos cargados
        self._from_dataframe = isinstance(input_path, pd.DataFrame)

    # Carga del dataset original
    def load_dataset(self):

        logger.info(f"Cargando dataset original desde: {self.input_path}")  # Log informativo de carga
        
        if isinstance(self.input_path, pd.DataFrame):
            self.df = self.input_path.copy()
            logger.debug("Dataset cargado desde DataFrame en memoria")
            return

        if self.input_path is None:
            raise ValueError("input_path es None: debe proporcionar una ruta o un DataFrame antes de llamar a load_dataset().")

        self.df = pd.read_csv(self.input_path)

        df_parkinson = self.df[self.df["Padecimiento"].str.contains("^Enfermedad de Parkinson", case=False, na=False)]

        self.histograma(df_parkinson,"Año")
        


        
    
    def histograma(self,df,columna):
        """
        Genera un histograma de la columna indicada y lo guarda en reports/figures.
        """

        imagen_salida = Path(conf["paths"]["figures"])
        
       
        # Conteo por valores únicos de la columna
        conteo = df.groupby(columna).size()

        # Graficar histograma
        plt.figure(figsize=(10, 6))
        conteo.plot(kind="bar", color="steelblue", edgecolor="black")

        plt.title(f"Distribución de {columna} - Enfermedad de Parkinson")
        plt.xlabel(columna)
        plt.ylabel("Frecuencia")
        plt.xticks(rotation=45)

        for i, value in enumerate(conteo):
            plt.text(i, value + 50, str(value), ha="center", va="bottom", fontsize=9)

        # Guardar figura
        output_file = imagen_salida / f"histograma_{columna}.png"
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()

        logger.info(f"Histograma guardado en: {output_file}")




        



    def run(self):
        self.load_dataset()   # Carga los datos (desde Path o DataFrame)
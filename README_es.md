# FootballPrediction

## Objetivo

Construir un modelo de Mahchine Learning para predecir el ganador de la Premier League inglesa (EPL) durante la temporada 2020-2021.

## Data

Las fuentes de información para construir el dataset final encontrado en **england-transformed.csv** las tomamos de: 
- Histórico de partidos: [jalapic/engsoccerdata](https://github.com/jalapic/engsoccerdata)  
- Valores en USD de los equipos [Transfermarkt](www.transfermarkt.com)

### Flujo de trabajo

### Cleaning Data
In this part of the project we drop some columns and add some columns. We consider that the week game,  

We remove FT, totgoal, goaldif because those columns can be obtain in function of others columns.

### Training

## Results

## Estructura del repositorio

- **data/**: contiene todos los csv's ocupados
    - **data_money/**: archivos csv relacionados con los valores en USD de los equipos de la EPL desde el 2005
- **data_transformation/**: archivos relacionados con la transformación de los datasets originales de las fuentes de información al dataset final que ocupamos para entrenar el modelo. 
    - **score_table/**: archivos de utilidad para construir el dataset final
        - **table.py**: estructuras de datos de utilidad para la transformación de la información (```ScoreTable```, ```Team```, ```HistoricScoreTable```)
        - **create.py**: contiene funciones de utilidad para crear un ```ScoreTable``` y realizar predicciones con base en el modelo entrenado. 
        - **metrics.py**: contiene las métricas personalizadas para evaluar dos ```ScoreTable```
    - **data_cleaning.ipynb**: limpiar el dataset de [jalapic/engsoccerdata](https://github.com/jalapic/engsoccerdata) y guardarlo en **england-clean.csv**. 
    - **feature_addition.py**: encargado de agregar columnas de utilidad para nuestro análisis (estas columnas aplican para equipos local y visitante)
        - puntos actuales en la tabla de posiciones
        - posición en la tabla de posiciones de la última temporada
        - posición en la tabla de posiciones de la penúltima temporada
    - **team_value.py**: agrega las columnas del valor en USD para los equipos local y visitante con base en la información de [Transfermarkt](www.transfermarkt.com).
    - **creating_data_2020.py**: crea información para predecir el 2020
- **future_prediction.py**: predice la tabla de posiciones (```ScoreTable```) para el 2020
- **model.ipynb**: entrena el modelo con base en el csv **england-transformed.csv** y obtiene las métricas de cada modelo entrenado
- **model_evaluation.py**: evaluá el modelo entrenado para diferentes temporadas
- **old_model.ipynb**: evaluación de varios modelos para un dataset que solo contiene fecha, equipo local, equipo visitante y resultado del partido
- **model.pkl**: almacena el archivo del modelo

### Flujo de ejecución
Instrucciones para ejecutar el proyecto: 
**Limpieza de datos**:
    - Ejecutar todas las celdas de **data_cleaning.ipynb**
**Entrenamiento**:
    - Crear el modelo ejecutando todas las celdas de **model.ipynb**
        - **Nota**: el paso anterior guarda el modelo en **model.pkl**
**Predicción 2020**:
    - Ejecutar **future_prediction.py**
**Predicción temporada a temporada**:
    - Ejecutar **model_evaluation.py**
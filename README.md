# Análisis de Churn de Clientes - Empresa de Telecomunicaciones

## Descripción del Problema de Negocio

Este proyecto aborda el **problema de churn (abandono) de clientes** en una empresa de telecomunicaciones. El churn de clientes es un indicador crítico que mide el porcentaje de clientes que cancelan su suscripción o dejan de utilizar los servicios durante un período determinado.

### Objetivo Principal
Desarrollar un modelo predictivo que permita identificar con antelación qué clientes tienen mayor probabilidad de abandonar el servicio, con el fin de:
- **Reducir la tasa de churn** mediante estrategias de retención dirigidas
- **Optimizar los recursos** enfocando los esfuerzos de retención en clientes de alto riesgo  
- **Maximizar el valor del ciclo de vida del cliente** (Customer Lifetime Value)
- **Mejorar la rentabilidad** reduciendo los costos de adquisición de nuevos clientes

## Dataset Utilizado

### Fuente de Datos
- **Archivo**: `telco_customer_churn.csv`
- **Tamaño**: 7,043 registros de clientes
- **Características**: 21 variables (20 predictoras + 1 variable objetivo)

### Descripción de Variables

#### Variables Demográficas
- `customerID`: Identificador único del cliente
- `gender`: Género del cliente (Male/Female)
- `SeniorCitizen`: Indica si es cliente senior (0/1)
- `Partner`: Tiene pareja (Yes/No)
- `Dependents`: Tiene dependientes (Yes/No)

#### Variables de Cuenta
- `tenure`: Meses como cliente de la empresa
- `Contract`: Tipo de contrato (Month-to-month, One year, Two year)
- `PaperlessBilling`: Facturación sin papel (Yes/No)
- `PaymentMethod`: Método de pago (Electronic check, Mailed check, Bank transfer, Credit card)
- `MonthlyCharges`: Cargos mensuales
- `TotalCharges`: Total de cargos acumulados

#### Variables de Servicios
- `PhoneService`: Servicio telefónico (Yes/No)
- `MultipleLines`: Múltiples líneas telefónicas (Yes/No/No phone service)
- `InternetService`: Servicio de internet (DSL, Fiber optic, No)
- `OnlineSecurity`: Seguridad online (Yes/No/No internet service)
- `OnlineBackup`: Respaldo online (Yes/No/No internet service)
- `DeviceProtection`: Protección de dispositivos (Yes/No/No internet service)
- `TechSupport`: Soporte técnico (Yes/No/No internet service)
- `StreamingTV`: TV en streaming (Yes/No/No internet service)
- `StreamingMovies`: Películas en streaming (Yes/No/No internet service)

#### Variable Objetivo
- `Churn`: Indica si el cliente abandonó el servicio (Yes/No)

## Metodología

### 1. Análisis Exploratorio de Datos (EDA)
- **Carga y exploración inicial** del dataset
- **Análisis de distribuciones** de variables categóricas y numéricas
- **Identificación de valores nulos** y datos inconsistentes
- **Análisis de correlaciones** entre variables
- **Visualización de patrones** de churn por diferentes segmentos

### 2. Preprocesamiento de Datos
- **Limpieza de datos**: Tratamiento de valores nulos y duplicados
- **Detección y tratamiento de outliers** usando método IQR
- **Conversión de tipos de datos** apropiados
- **Ingeniería de características**: Creación de nuevas variables derivadas
- **Codificación de variables categóricas**: One-Hot Encoding y Label Encoding
- **Normalización y escalado** de variables numéricas

### 3. Modelado y Evaluación
- **División del dataset**: 80% entrenamiento, 20% prueba
- **Validación cruzada** para evaluación robusta de modelos
- **Métricas de evaluación**:
  - Accuracy (Precisión)
  - Precision (Precisión por clase)
  - Recall (Sensibilidad)
  - F1-Score (Media armónica entre precision y recall)
  - AUC-ROC (Área bajo la curva ROC)

### 4. Análisis de Negocio
- **Interpretación de características más importantes**
- **Análisis de segmentación de riesgo** de clientes
- **Evaluación del impacto económico** de las predicciones
- **Recomendaciones estratégicas** basadas en los hallazgos

## Modelos Probados

### 1. **Regresión Logística**
- **Propósito**: Modelo base e interpretable
- **Ventajas**: Fácil interpretación, rápido entrenamiento
- **Uso**: Referencia para comparación con modelos más complejos

### 2. **Random Forest**
- **Propósito**: Modelo ensemble robusto
- **Ventajas**: Manejo automático de outliers, importancia de características
- **Parámetros**: Configuración por defecto con random_state=42

### 3. **LightGBM**
- **Propósito**: Gradient boosting eficiente
- **Ventajas**: Rápido entrenamiento, buen rendimiento en datos tabulares
- **Características**: Optimizado para velocidad y eficiencia de memoria

### 4. **Support Vector Machine (SVM)**
- **Propósito**: Clasificador con kernel por defecto
- **Ventajas**: Efectivo en espacios de alta dimensionalidad
- **Consideraciones**: Puede ser lento en datasets grandes

### 5. **XGBoost**
- **Propósito**: Gradient boosting de alto rendimiento
- **Ventajas**: Excelente rendimiento en competencias, regularización incorporada
- **Características**: Optimización avanzada de hiperparámetros

## Resultados Principales

### Rendimiento de Modelos
Los modelos fueron evaluados usando validación cruzada de 5 folds, obteniéndose los siguientes resultados comparativos:

- **Métricas clave evaluadas**: Accuracy, Precision, Recall, F1-Score, AUC
- **Mejor modelo**: Determinado por F1-Score promedio en validación cruzada
- **Análisis de matriz de confusión** para evaluar tipos de errores

### Características Más Importantes
Las variables con mayor poder predictivo para el churn incluyen:
- **Tenure**: Duración de la relación con el cliente
- **Contract**: Tipo de contrato (mes a mes vs. contratos largos)
- **TotalCharges**: Valor total pagado por el cliente
- **MonthlyCharges**: Cargos mensuales del servicio
- **PaymentMethod**: Método de pago preferido

### Segmentación de Riesgo
Los clientes se clasifican en tres categorías de riesgo:
- **Alto riesgo**: Probabilidad de churn > 70%
- **Riesgo medio**: Probabilidad de churn entre 30-70%
- **Bajo riesgo**: Probabilidad de churn < 30%

### Impacto de Negocio
- **Falsos Positivos (FP)**: Costo de promociones innecesarias
- **Falsos Negativos (FN)**: Pérdida de clientes no identificados
- **ROI estimado**: Análisis de retorno de inversión de estrategias de retención

## Conclusiones

### Hallazgos Clave
1. **Contratos mes a mes** presentan significativamente mayor riesgo de churn
2. **Clientes con menor tenure** requieren atención prioritaria
3. **Método de pago** es un indicador importante del comportamiento del cliente
4. **Servicios adicionales** (streaming, soporte técnico) correlacionan con menor churn

### Recomendaciones Estratégicas
1. **Incentivos para contratos largos**: Promociones para migrar de mes a mes a anuales
2. **Programa de fidelización temprana**: Atención especial en los primeros meses
3. **Mejora de métodos de pago**: Facilitar pagos automáticos
4. **Cross-selling inteligente**: Ofrecer servicios complementarios basado en perfil

### Limitaciones del Modelo
- **Datos históricos**: El modelo se basa en patrones pasados que pueden cambiar
- **Desbalance de clases**: Puede afectar la precisión en la clase minoritaria
- **Interpretación contextual**: Requiere validación continua con equipos de negocio

## Instrucciones para Reproducir el Análisis

### Prerrequisitos
```bash
# Dependencias de Python requeridas:
pandas
numpy
matplotlib
seaborn
scikit-learn
lightgbm
xgboost
jupyter
```

### Instalación de Dependencias
```bash
# Instalar dependencias básicas
pip install pandas numpy matplotlib seaborn scikit-learn jupyter

# Instalar bibliotecas de ML adicionales
pip install lightgbm xgboost
```

### Ejecución del Análisis

1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd Portafolio
   ```

2. **Verificar archivos necesarios**:
   - Asegúrate de que `Main.ipynb` y `telco_customer_churn.csv` estén en el directorio

3. **Ejecutar Jupyter Notebook**:
   ```bash
   jupyter notebook Main.ipynb
   ```

4. **Ejecutar celdas secuencialmente**:
   - Ejecuta todas las celdas en orden desde el principio
   - El análisis completo toma aproximadamente 15-20 minutos
   - Algunos modelos (como SVM) pueden requerir más tiempo de entrenamiento

### Estructura del Notebook
- **Celdas 1-15**: Carga de datos y análisis exploratorio
- **Celdas 16-30**: Preprocesamiento y limpieza de datos
- **Celdas 31-45**: Entrenamiento de modelos
- **Celdas 46-63**: Evaluación, comparación y análisis de negocio

### Outputs Esperados
- **Visualizaciones**: Gráficos de distribuciones, correlaciones, y métricas
- **Tablas de resultados**: Métricas de rendimiento por modelo
- **Análisis de importancia**: Variables más influyentes en las predicciones
- **Recomendaciones**: Insights accionables para estrategias de retención

### Personalización
Para adaptar el análisis a otros datasets:
1. Reemplaza `telco_customer_churn.csv` con tu dataset
2. Ajusta las columnas categóricas y numéricas según corresponda
3. Modifica la variable objetivo si es necesaria
4. Adapta las visualizaciones y análisis de negocio al contexto específico

---

**Nota**: Este análisis está diseñado para proporcionar insights accionables sobre retención de clientes. Los resultados deben interpretarse en el contexto específico del negocio y validarse continuamente con datos actualizados.
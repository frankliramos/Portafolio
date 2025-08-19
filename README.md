# Portafolio de Análisis de Datos
Portfolio de trabajo con análisis avanzado de datos y segmentación de clientes

## 🎯 Proyecto Principal: Segmentación de Clientes por Riesgo

### Descripción
Implementación de una estrategia integral de segmentación de clientes basada en evaluación de riesgo para el dataset de Telco. El sistema categoriza a 7,043 clientes en diferentes segmentos de riesgo para marketing dirigido, gestión de riesgo y personalización de servicios.

### Características Principales
- **Análisis de Riesgo Multi-factor**: Combina probabilidad de churn, patrones de ingresos, estabilidad contractual y comportamiento de pago
- **Segmentación Automática**: Categoriza clientes en 4 niveles de riesgo (Crítico, Alto, Medio, Bajo)
- **Recomendaciones Estratégicas**: Proporciona acciones específicas para cada segmento
- **Visualizaciones Interactivas**: Dashboard completo con gráficos y métricas clave
- **Exportación de Resultados**: Genera reportes ejecutivos y datos para implementación

### Archivos del Proyecto

#### 📊 Análisis Principal
- `customer_risk_segmentation.py` - Sistema completo de segmentación de riesgo
- `Customer_Risk_Segmentation_Interactive.ipynb` - Notebook interactivo para análisis
- `Telco esp.ipynb` - Análisis original de churn de clientes

#### 📈 Resultados Generados
- `customer_risk_segmentation_full_data.csv` - Dataset completo con puntuaciones de riesgo
- `customer_risk_segmentation_summary.csv` - Estadísticas por segmento
- `customer_risk_segmentation_analysis.png` - Dashboard de visualizaciones
- `CUSTOMER_RISK_SEGMENTATION_REPORT.md` - Reporte ejecutivo detallado
- `risk_segmentation_dashboard.html` - Dashboard web interactivo

#### 📁 Datos
- `telco_customer_churn.csv` - Dataset original de clientes Telco (7,043 registros)

### Resultados Clave

#### Distribución de Segmentos de Riesgo
- **Riesgo Crítico**: 405 clientes (5.8%) - Acción inmediata requerida
- **Riesgo Alto**: 2,921 clientes (41.5%) - Intervención proactiva necesaria
- **Riesgo Medio**: 1,848 clientes (26.2%) - Monitorear y nutrir
- **Riesgo Bajo**: 1,869 clientes (26.5%) - Mantener y hacer crecer

#### Impacto Financiero
- **Ingresos Mensuales en Riesgo**: $317,487
- **Ingresos Anuales en Riesgo**: $3,809,844
- **Clientes que Requieren Atención Inmediata**: 3,326 (47.3%)

### Metodología de Puntuación de Riesgo

El algoritmo de puntuación (0-100) combina:
- **Riesgo de Churn (40%)**: Comportamiento real de churn cuando está disponible
- **Riesgo Contractual (30%)**: Contratos mes-a-mes vs. contratos a largo plazo
- **Riesgo de Ingresos (30%)**: Patrones de pago y volatilidad de cargos
- **Factores Adicionales**: Tenencia, método de pago, demografía

### Recomendaciones Estratégicas por Segmento

#### 🚨 Riesgo Crítico - ACCIÓN INMEDIATA
- Desplegar especialistas en retención para contacto personal
- Ofrecer paquetes especiales de retención y recompensas de lealtad
- Cambiar a planes de pago anuales con descuentos
- Proporcionar soporte premium al cliente

#### ⚠️ Riesgo Alto - INTERVENCIÓN PROACTIVA
- Implementar campañas de retención dirigidas
- Ofrecer incentivos de actualización de contrato
- Enviar encuestas de satisfacción y actuar sobre la retroalimentación
- Monitorear patrones de uso para señales de alerta temprana

#### 📊 Riesgo Medio - MONITOREAR Y NUTRIR
- Comunicaciones regulares de seguimiento y boletines
- Ofrecer recomendaciones de optimización de servicios
- Proporcionar contenido educativo sobre beneficios
- Ofrecer incentivos moderados de lealtad

#### ✅ Riesgo Bajo - MANTENER Y CRECER
- Enfocarse en oportunidades de venta adicional y cruzada
- Usar como defensores para programas de referencia
- Recopilar testimonios y casos de estudio
- Considerar para pruebas beta de nuevos servicios

### Cómo Usar

#### Análisis Rápido
```python
from customer_risk_segmentation import CustomerRiskSegmentation

# Inicializar sistema de segmentación
segmentation = CustomerRiskSegmentation('telco_customer_churn.csv')

# Ejecutar análisis completo
segmented_data, segments = segmentation.run_complete_analysis()
```

#### Análisis Interactivo
Abrir `Customer_Risk_Segmentation_Interactive.ipynb` en Jupyter Notebook

#### Dashboard Web
Abrir `risk_segmentation_dashboard.html` en un navegador web

### Tecnologías Utilizadas
- **Python**: Pandas, NumPy, Scikit-learn
- **Visualización**: Matplotlib, Seaborn
- **Machine Learning**: Clustering, Random Forest
- **Web**: HTML, CSS para dashboard

### Roadmap de Implementación
1. **Semana 1**: Desplegar intervenciones inmediatas para segmento de Riesgo Crítico
2. **Semana 2-3**: Lanzar campañas de retención para clientes de Alto Riesgo
3. **Mes 1**: Implementar sistemas de monitoreo para Riesgo Medio
4. **Continuo**: Mantener estrategias de crecimiento para clientes de Bajo Riesgo

### Métricas de Éxito
- Reducción de tasa de churn mensual del 15-20%
- Tasa de conversión de contratos del 25%+ para clientes de riesgo medio
- Optimización de método de pago para 50%+ de usuarios de cheque electrónico de alto riesgo

---
*Análisis completado usando algoritmo de puntuación de riesgo multi-factor en 7,043 clientes de Telco*

#!/usr/bin/env python3
"""
Generador de Visualizaciones para Dashboard EDA
Crea los gráficos principales del análisis de churn de clientes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo profesional
plt.style.use('default')
sns.set_palette("Set2")

# Colores corporativos consistentes
PRIMARY_COLOR = '#2E86AB'      # Azul profesional
SECONDARY_COLOR = '#A23B72'    # Rosa/magenta
ACCENT_COLOR = '#F18F01'       # Naranja
SUCCESS_COLOR = '#C73E1D'      # Rojo para churn
NEUTRAL_COLOR = '#6C757D'      # Gris

# Configuración global de figuras
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 11
})

def load_and_clean_data():
    """Carga y limpia los datos"""
    df = pd.read_csv('telco_customer_churn.csv')
    
    # Limpieza básica de datos
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    
    # Conversión de variables categóricas a numéricas para análisis
    df['Churn_Binary'] = df['Churn'].map({'Yes': 1, 'No': 0})
    df['SeniorCitizen_Label'] = df['SeniorCitizen'].map({1: 'Sí', 0: 'No'})
    
    return df

def create_contract_analysis(df):
    """Gráfico 1: Análisis de Contratos"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Subplot 1: Distribución de contratos
    contract_dist = df['Contract'].value_counts()
    colors1 = [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR]
    wedges, texts, autotexts = ax1.pie(contract_dist.values, labels=contract_dist.index, 
                                       autopct='%1.1f%%', colors=colors1, startangle=90)
    ax1.set_title('Distribución de Tipos de Contrato', fontsize=14, fontweight='bold', pad=20)
    
    # Subplot 2: Tasa de churn por contrato
    churn_by_contract = df.groupby('Contract')['Churn_Binary'].agg(['count', 'sum', 'mean']).reset_index()
    churn_by_contract['churn_rate'] = churn_by_contract['mean'] * 100
    
    bars = ax2.bar(churn_by_contract['Contract'], churn_by_contract['churn_rate'], 
                   color=[SUCCESS_COLOR, ACCENT_COLOR, PRIMARY_COLOR], alpha=0.8)
    
    # Añadir etiquetas de valores
    for bar, rate in zip(bars, churn_by_contract['churn_rate']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title('Tasa de Churn por Tipo de Contrato', fontsize=14, fontweight='bold', pad=20)
    ax2.set_ylabel('Tasa de Churn (%)', fontsize=12)
    ax2.set_ylim(0, max(churn_by_contract['churn_rate']) * 1.2)
    
    plt.tight_layout()
    plt.savefig('chart1_contract_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico 1 - Análisis de Contratos creado")

def create_tenure_analysis(df):
    """Gráfico 2: Análisis de Permanencia"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Subplot 1: Distribución de permanencia por churn
    df_no_churn = df[df['Churn'] == 'No']['tenure']
    df_churn = df[df['Churn'] == 'Yes']['tenure']
    
    ax1.hist(df_no_churn, bins=30, alpha=0.7, label='No Churn', color=PRIMARY_COLOR, density=True)
    ax1.hist(df_churn, bins=30, alpha=0.7, label='Churn', color=SUCCESS_COLOR, density=True)
    ax1.set_xlabel('Permanencia (meses)', fontsize=12)
    ax1.set_ylabel('Densidad', fontsize=12)
    ax1.set_title('Distribución de Permanencia por Estado de Churn', fontsize=14, fontweight='bold', pad=20)
    ax1.legend()
    
    # Subplot 2: Tasa de churn por grupos de permanencia
    df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 36, 48, 72], 
                               labels=['0-12m', '13-24m', '25-36m', '37-48m', '49-72m'])
    
    churn_by_tenure = df.groupby('tenure_group')['Churn_Binary'].agg(['count', 'mean']).reset_index()
    churn_by_tenure['churn_rate'] = churn_by_tenure['mean'] * 100
    
    bars = ax2.bar(range(len(churn_by_tenure)), churn_by_tenure['churn_rate'],
                   color=[SUCCESS_COLOR if x > 30 else ACCENT_COLOR if x > 15 else PRIMARY_COLOR 
                          for x in churn_by_tenure['churn_rate']], alpha=0.8)
    
    # Añadir etiquetas
    for i, (bar, rate) in enumerate(zip(bars, churn_by_tenure['churn_rate'])):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_xticks(range(len(churn_by_tenure)))
    ax2.set_xticklabels(churn_by_tenure['tenure_group'])
    ax2.set_xlabel('Grupos de Permanencia', fontsize=12)
    ax2.set_ylabel('Tasa de Churn (%)', fontsize=12)
    ax2.set_title('Tasa de Churn por Permanencia', fontsize=14, fontweight='bold', pad=20)
    ax2.set_ylim(0, max(churn_by_tenure['churn_rate']) * 1.2)
    
    plt.tight_layout()
    plt.savefig('chart2_tenure_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico 2 - Análisis de Permanencia creado")

def create_payment_analysis(df):
    """Gráfico 3: Análisis de Métodos de Pago"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Subplot 1: Distribución de métodos de pago
    payment_dist = df['PaymentMethod'].value_counts()
    colors_payment = [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, SUCCESS_COLOR]
    
    wedges, texts, autotexts = ax1.pie(payment_dist.values, labels=payment_dist.index, 
                                       autopct='%1.1f%%', colors=colors_payment, startangle=90)
    ax1.set_title('Distribución de Métodos de Pago', fontsize=14, fontweight='bold', pad=20)
    
    # Subplot 2: Tasa de churn por método de pago
    churn_by_payment = df.groupby('PaymentMethod')['Churn_Binary'].agg(['count', 'mean']).reset_index()
    churn_by_payment['churn_rate'] = churn_by_payment['mean'] * 100
    churn_by_payment = churn_by_payment.sort_values('churn_rate', ascending=True)
    
    bars = ax2.barh(range(len(churn_by_payment)), churn_by_payment['churn_rate'],
                    color=[PRIMARY_COLOR if 'automatic' in method.lower() else SUCCESS_COLOR 
                           for method in churn_by_payment['PaymentMethod']], alpha=0.8)
    
    # Añadir etiquetas
    for i, (bar, rate) in enumerate(zip(bars, churn_by_payment['churn_rate'])):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                 f'{rate:.1f}%', ha='left', va='center', fontweight='bold')
    
    ax2.set_yticks(range(len(churn_by_payment)))
    ax2.set_yticklabels([method.replace(' (automatic)', '\n(automático)').replace(' ', '\n') 
                         for method in churn_by_payment['PaymentMethod']])
    ax2.set_xlabel('Tasa de Churn (%)', fontsize=12)
    ax2.set_title('Tasa de Churn por Método de Pago', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlim(0, max(churn_by_payment['churn_rate']) * 1.2)
    
    plt.tight_layout()
    plt.savefig('chart3_payment_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico 3 - Análisis de Métodos de Pago creado")

def create_services_analysis(df):
    """Gráfico 4: Análisis de Servicios Adicionales"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Servicios a analizar
    services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    service_names = ['Seguridad\nOnline', 'Backup\nOnline', 'Protección\nDispositivos', 
                     'Soporte\nTécnico', 'Streaming\nTV', 'Streaming\nPelículas']
    
    # Calcular tasa de churn por servicio
    service_churn_rates = []
    for service in services:
        service_data = df[df[service] != 'No internet service']
        churn_rate = service_data[service_data[service] == 'Yes']['Churn_Binary'].mean() * 100
        service_churn_rates.append(churn_rate)
    
    # Subplot 1: Tasa de churn por servicio
    bars = ax1.bar(range(len(services)), service_churn_rates, 
                   color=[SECONDARY_COLOR if rate < 20 else ACCENT_COLOR if rate < 30 else SUCCESS_COLOR 
                          for rate in service_churn_rates], alpha=0.8)
    
    for i, (bar, rate) in enumerate(zip(bars, service_churn_rates)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_xticks(range(len(services)))
    ax1.set_xticklabels(service_names, rotation=45, ha='right')
    ax1.set_ylabel('Tasa de Churn (%)', fontsize=12)
    ax1.set_title('Tasa de Churn por Servicio Adicional\n(Solo clientes con Internet)', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.set_ylim(0, max(service_churn_rates) * 1.2)
    
    # Subplot 2: Número de servicios vs churn
    df_internet = df[df['InternetService'] != 'No'].copy()
    df_internet['num_services'] = 0
    
    for service in services:
        df_internet['num_services'] += (df_internet[service] == 'Yes').astype(int)
    
    service_count_churn = df_internet.groupby('num_services')['Churn_Binary'].agg(['count', 'mean']).reset_index()
    service_count_churn['churn_rate'] = service_count_churn['mean'] * 100
    
    bars2 = ax2.bar(service_count_churn['num_services'], service_count_churn['churn_rate'],
                    color=[SUCCESS_COLOR if rate > 40 else ACCENT_COLOR if rate > 25 else PRIMARY_COLOR 
                           for rate in service_count_churn['churn_rate']], alpha=0.8)
    
    for bar, rate in zip(bars2, service_count_churn['churn_rate']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_xlabel('Número de Servicios Adicionales', fontsize=12)
    ax2.set_ylabel('Tasa de Churn (%)', fontsize=12)
    ax2.set_title('Impacto del Número de Servicios en el Churn\n(Clientes con Internet)', 
                  fontsize=14, fontweight='bold', pad=20)
    ax2.set_ylim(0, max(service_count_churn['churn_rate']) * 1.2)
    
    plt.tight_layout()
    plt.savefig('chart4_services_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico 4 - Análisis de Servicios creado")

def create_demographic_analysis(df):
    """Gráfico 5: Análisis Demográfico"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Subplot 1: Churn por género
    gender_churn = df.groupby('gender')['Churn_Binary'].agg(['count', 'mean']).reset_index()
    gender_churn['churn_rate'] = gender_churn['mean'] * 100
    
    bars1 = ax1.bar(gender_churn['gender'], gender_churn['churn_rate'],
                    color=[PRIMARY_COLOR, SECONDARY_COLOR], alpha=0.8)
    
    for bar, rate in zip(bars1, gender_churn['churn_rate']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_title('Tasa de Churn por Género', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Tasa de Churn (%)')
    
    # Subplot 2: Churn por estado senior
    senior_churn = df.groupby('SeniorCitizen_Label')['Churn_Binary'].agg(['count', 'mean']).reset_index()
    senior_churn['churn_rate'] = senior_churn['mean'] * 100
    
    bars2 = ax2.bar(senior_churn['SeniorCitizen_Label'], senior_churn['churn_rate'],
                    color=[PRIMARY_COLOR, SUCCESS_COLOR], alpha=0.8)
    
    for bar, rate in zip(bars2, senior_churn['churn_rate']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title('Tasa de Churn por Estado Senior', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tasa de Churn (%)')
    ax2.set_xlabel('Cliente Senior')
    
    # Subplot 3: Churn por dependientes
    dependents_churn = df.groupby('Dependents')['Churn_Binary'].agg(['count', 'mean']).reset_index()
    dependents_churn['churn_rate'] = dependents_churn['mean'] * 100
    
    bars3 = ax3.bar(dependents_churn['Dependents'], dependents_churn['churn_rate'],
                    color=[SUCCESS_COLOR, PRIMARY_COLOR], alpha=0.8)
    
    for bar, rate in zip(bars3, dependents_churn['churn_rate']):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax3.set_title('Tasa de Churn por Dependientes', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Tasa de Churn (%)')
    ax3.set_xlabel('Tiene Dependientes')
    
    # Subplot 4: Distribución de cargos mensuales por churn
    ax4.hist(df[df['Churn'] == 'No']['MonthlyCharges'], bins=30, alpha=0.7, 
             label='No Churn', color=PRIMARY_COLOR, density=True)
    ax4.hist(df[df['Churn'] == 'Yes']['MonthlyCharges'], bins=30, alpha=0.7, 
             label='Churn', color=SUCCESS_COLOR, density=True)
    
    ax4.axvline(df[df['Churn'] == 'No']['MonthlyCharges'].mean(), color=PRIMARY_COLOR, 
                linestyle='--', linewidth=2, label=f'Media No Churn: ${df[df["Churn"] == "No"]["MonthlyCharges"].mean():.1f}')
    ax4.axvline(df[df['Churn'] == 'Yes']['MonthlyCharges'].mean(), color=SUCCESS_COLOR, 
                linestyle='--', linewidth=2, label=f'Media Churn: ${df[df["Churn"] == "Yes"]["MonthlyCharges"].mean():.1f}')
    
    ax4.set_title('Distribución de Cargos Mensuales', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Cargos Mensuales ($)')
    ax4.set_ylabel('Densidad')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('chart5_demographic_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico 5 - Análisis Demográfico creado")

def create_correlation_analysis(df):
    """Gráfico 6: Análisis de Correlaciones"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    
    # Preparar datos para correlación
    df_corr = df.copy()
    categorical_mappings = {
        'gender': {'Male': 1, 'Female': 0},
        'Partner': {'Yes': 1, 'No': 0},
        'Dependents': {'Yes': 1, 'No': 0},
        'PhoneService': {'Yes': 1, 'No': 0},
        'PaperlessBilling': {'Yes': 1, 'No': 0},
        'Contract': {'Month-to-month': 2, 'One year': 1, 'Two year': 0},
        'InternetService': {'Fiber optic': 2, 'DSL': 1, 'No': 0},
        'PaymentMethod': {'Electronic check': 3, 'Mailed check': 2, 'Bank transfer (automatic)': 1, 'Credit card (automatic)': 0}
    }
    
    for col, mapping in categorical_mappings.items():
        df_corr[col] = df_corr[col].map(mapping)
    
    # Seleccionar variables clave para correlación
    corr_vars = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Contract', 'PaymentMethod', 
                 'InternetService', 'SeniorCitizen', 'Partner', 'Dependents', 'PaperlessBilling', 'Churn_Binary']
                 
    corr_matrix = df_corr[corr_vars].corr()
    
    # Subplot 1: Mapa de calor de correlaciones
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap=cmap, center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax1, fmt='.2f')
    ax1.set_title('Mapa de Calor - Correlaciones con Churn', fontsize=14, fontweight='bold', pad=20)
    
    # Subplot 2: Top factores de riesgo
    churn_corr = corr_matrix['Churn_Binary'].abs().drop('Churn_Binary').sort_values(ascending=True)
    top_factors = churn_corr.tail(8)
    
    colors_factors = [SUCCESS_COLOR if x > 0.3 else ACCENT_COLOR if x > 0.15 else PRIMARY_COLOR for x in top_factors.values]
    bars_factors = ax2.barh(range(len(top_factors)), top_factors.values, color=colors_factors, alpha=0.8)
    
    # Añadir etiquetas
    for i, (bar, corr_val) in enumerate(zip(bars_factors, top_factors.values)):
        ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                 f'{corr_val:.3f}', ha='left', va='center', fontweight='bold')
    
    factor_labels = {
        'tenure': 'Permanencia',
        'Contract': 'Tipo de Contrato',
        'PaymentMethod': 'Método de Pago',
        'TotalCharges': 'Cargos Totales',
        'MonthlyCharges': 'Cargos Mensuales',
        'InternetService': 'Servicio Internet',
        'PaperlessBilling': 'Facturación Digital',
        'SeniorCitizen': 'Cliente Senior'
    }
    
    ax2.set_yticks(range(len(top_factors)))
    ax2.set_yticklabels([factor_labels.get(factor, factor) for factor in top_factors.index])
    ax2.set_xlabel('Correlación Absoluta con Churn', fontsize=12)
    ax2.set_title('Factores de Riesgo Principales\n(Correlación con Churn)', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlim(0, max(top_factors.values) * 1.2)
    
    plt.tight_layout()
    plt.savefig('chart6_correlation_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Gráfico 6 - Análisis de Correlaciones creado")

def main():
    """Función principal"""
    print("🚀 Iniciando generación de Dashboard EDA...")
    
    # Cargar datos
    df = load_and_clean_data()
    print(f"📊 Dataset cargado: {df.shape[0]:,} clientes con {df.shape[1]} variables")
    
    # Crear todos los gráficos
    create_contract_analysis(df)
    create_tenure_analysis(df)
    create_payment_analysis(df)
    create_services_analysis(df)
    create_demographic_analysis(df)
    create_correlation_analysis(df)
    
    # Estadísticas finales
    churn_rate = df['Churn_Binary'].mean() * 100
    avg_monthly = df['MonthlyCharges'].mean()
    avg_tenure = df['tenure'].mean()
    
    print("\n" + "="*60)
    print("📈 ESTADÍSTICAS CLAVE GENERADAS:")
    print("="*60)
    print(f"📊 Tasa de Churn General: {churn_rate:.1f}%")
    print(f"💰 Ingreso Mensual Promedio: ${avg_monthly:.2f}")
    print(f"🕐 Permanencia Promedio: {avg_tenure:.1f} meses")
    print(f"🎯 Total de Clientes Analizados: {df.shape[0]:,}")
    print("="*60)
    print("✅ Dashboard EDA completado exitosamente!")
    print("📁 Archivos generados:")
    print("   • EDA_Dashboard.html (Dashboard interactivo)")
    print("   • EDA_Dashboard.ipynb (Notebook ejecutable)")
    print("   • chart1_contract_analysis.png")
    print("   • chart2_tenure_analysis.png") 
    print("   • chart3_payment_analysis.png")
    print("   • chart4_services_analysis.png")
    print("   • chart5_demographic_analysis.png")
    print("   • chart6_correlation_analysis.png")

if __name__ == "__main__":
    main()
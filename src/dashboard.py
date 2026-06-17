"""
Dashboard Interactivo — TPI Análisis de Rendimiento Académico
==============================================================
Requiere: streamlit, pandas, matplotlib, seaborn
Ejecución: streamlit run src/dashboard.py

El dashboard aplica el pipeline ETL internamente (limpieza + features),
leyendo directamente el CSV crudo. No depende de un archivo pre-limpio.
"""

import os
import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path
# para que `from src.etl import ...` funcione correctamente
# sin importar desde qué directorio se ejecute streamlit
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.etl import cargar_csv, limpiar, tratar_outliers, crear_features

# -----------------------------------------------------------------------------
# Configuración de página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Academico — TPI",
    page_icon="📊",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Funciones auxiliares de visualización
# -----------------------------------------------------------------------------
def configurar_estilo_dash():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "figure.figsize": (10, 5),
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "font.size": 10,
    })


def plot_calificaciones(df_sel: pd.DataFrame) -> plt.Figure:
    """Grafico 1: Conteo de calificaciones (orden A→F)."""
    configurar_estilo_dash()
    orden = ["A", "B", "C", "D", "F"]
    fig, ax = plt.subplots(figsize=(9, 5))
    counts = df_sel["calificacion"].value_counts().reindex(orden, fill_value=0)
    palette = {"A": "#2ecc71", "B": "#3498db", "C": "#f1c40f", "D": "#e67e22", "F": "#e74c3c"}
    sns.barplot(x=counts.index, y=counts.values, palette=palette, ax=ax)
    ax.set_title("Distribucion de Calificaciones")
    ax.set_xlabel("Calificacion")
    ax.set_ylabel("Cantidad de Estudiantes")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 1, str(v), ha="center", fontweight="bold")
    plt.tight_layout()
    return fig


def plot_puntaje_por_departamento(df_sel: pd.DataFrame) -> plt.Figure:
    """Grafico 2: Distribucion del puntaje total por departamento."""
    configurar_estilo_dash()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(
        data=df_sel,
        x="departamento",
        y="puntaje_total",
        hue="departamento",
        palette="Set2",
        legend=False,
        ax=ax,
    )
    ax.set_title("Puntaje Total por Departamento")
    ax.set_xlabel("Departamento")
    ax.set_ylabel("Puntaje Total")
    plt.tight_layout()
    return fig


def plot_burbuja_estres_sueno(df_sel: pd.DataFrame) -> plt.Figure:
    """Grafico 4: Bubble chart — horas de sueño vs puntaje total,
    tamano de burbuja = nivel de estres, color = departamento."""
    configurar_estilo_dash()
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.scatterplot(
        data=df_sel,
        x="horas_sueno",
        y="puntaje_total",
        size="nivel_estres",
        sizes=(20, 200),
        hue="departamento",
        alpha=0.5,
        ax=ax,
        legend="brief",
    )
    sns.regplot(
        data=df_sel,
        x="horas_sueno",
        y="puntaje_total",
        scatter=False,
        color="black",
        line_kws={"linewidth": 2, "linestyle": "--"},
        ax=ax,
    )
    ax.set_title("Horas de Sueño vs Puntaje Total — Tamano segun Nivel de Estres")
    ax.set_xlabel("Horas de Sueño por Noche")
    ax.set_ylabel("Puntaje Total")
    ax.legend(title="Departamento / Estres", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    return fig


def plot_riesgo_por_calificacion(df_sel: pd.DataFrame) -> plt.Figure:
    """Grafico 3: Indice de riesgo por calificacion."""
    configurar_estilo_dash()
    orden = ["A", "B", "C", "D", "F"]
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(
        data=df_sel,
        x="calificacion",
        y="indice_riesgo",
        order=orden,
        palette="RdYlGn_r",
        ax=ax,
    )
    ax.set_title("Indice de Riesgo por Calificacion")
    ax.set_xlabel("Calificacion")
    ax.set_ylabel("Indice de Riesgo (0-100)")
    plt.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# Carga y transformacion de datos con cache
# El dashboard aplica el pipeline ETL internamente para no depender
# de un CSV pre-limpio. Solo requiere el CSV crudo original.
# -----------------------------------------------------------------------------
@st.cache_data
def cargar_y_transformar(ruta: str = "Students_Performance_Dataset.csv") -> pd.DataFrame:
    """Pipeline ETL completo: carga -> limpieza -> outliers -> features."""
    COLUMNAS_OUTLIERS = [
        "asistencia", "nota_parcial", "nota_final",
        "promedio_tps", "promedio_quizzes", "puntaje_participacion",
        "puntaje_proyectos", "puntaje_total", "horas_estudio_semanal",
        "horas_sueno",
    ]
    try:
        # 1. Carga y renombrado de columnas (espanol)
        df = cargar_csv(ruta)
        # 2. Limpieza: duplicados, strings, nulos
        df = limpiar(df)
        # 3. Outliers IQR
        df, _ = tratar_outliers(df, COLUMNAS_OUTLIERS)
        # 4. Feature engineering
        df = crear_features(df)
        return df
    except FileNotFoundError:
        st.error(
            f"No se encontro el archivo '{ruta}'. "
            "Asegurate de ejecutar el dashboard desde la raiz del proyecto."
        )
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error durante el pipeline ETL: {e}")
        return pd.DataFrame()


# -----------------------------------------------------------------------------
# Construccion del dashboard
# -----------------------------------------------------------------------------
st.title("📊 Dashboard — Rendimiento Academico")
st.markdown(
    "Panel de control interactivo para explorar el rendimiento de los estudiantes. "
    "Aplicá los filtros en el menu lateral para analizar subgrupos especificos."
)

# Carga de datos (pipeline ETL interno)
df = cargar_y_transformar()

if df.empty:
    st.stop()

# -------------------------------------------------------------------------
# Sidebar — Filtros
# -------------------------------------------------------------------------
st.sidebar.header("Filtros de busqueda")

departamentos = st.sidebar.multiselect(
    "Departamento",
    options=sorted(df["departamento"].dropna().unique()),
    default=sorted(df["departamento"].dropna().unique()),
)

generos = st.sidebar.multiselect(
    "Genero",
    options=sorted(df["genero"].dropna().unique()),
    default=sorted(df["genero"].dropna().unique()),
)

ingreso_opciones = ["Bajo", "Medio", "Alto"]
ingreso_seleccionado = st.sidebar.multiselect(
    "Nivel de Ingreso Familiar",
    options=ingreso_opciones,
    default=ingreso_opciones,
)

esfuerzo_opciones = ["Bajo", "Medio", "Alto"]
esfuerzo_seleccionado = st.sidebar.multiselect(
    "Nivel de Esfuerzo",
    options=esfuerzo_opciones,
    default=esfuerzo_opciones,
)

calif_opciones = ["A", "B", "C", "D", "F"]
calif_seleccionada = st.sidebar.multiselect(
    "Calificacion",
    options=calif_opciones,
    default=calif_opciones,
)

asistencia_min = st.sidebar.slider(
    "Asistencia minima (%)",
    min_value=0,
    max_value=100,
    value=0,
    step=5,
)

edad_min_val = int(df["edad"].min())
edad_max_val = int(df["edad"].max())
edad_rango = st.sidebar.slider(
    "Rango de Edad",
    min_value=edad_min_val,
    max_value=edad_max_val,
    value=(edad_min_val, edad_max_val),
    step=1,
)

# -------------------------------------------------------------------------
# Aplicar filtros
# -------------------------------------------------------------------------
df_filt = df[
    df["departamento"].isin(departamentos)
    & df["genero"].isin(generos)
    & df["ingreso_familiar"].isin(ingreso_seleccionado)
    & df["categoria_esfuerzo"].isin(esfuerzo_seleccionado)
    & df["calificacion"].isin(calif_seleccionada)
    & (df["asistencia"] >= asistencia_min)
    & (df["edad"] >= edad_rango[0])
    & (df["edad"] <= edad_rango[1])
].copy()

# -------------------------------------------------------------------------
# KPI — Metricas principales
# -------------------------------------------------------------------------
st.markdown("### Indicadores Clave (KPIs)")

total_est = len(df_filt)
promedio = df_filt["puntaje_total"].mean() if total_est > 0 else 0
aprobados = len(df_filt[df_filt["calificacion"].isin(["A", "B", "C", "D"])])
tasa_aprob = (aprobados / total_est * 100) if total_est > 0 else 0
riesgo_alto = (
    len(df_filt[df_filt["indice_riesgo"] >= 66]) / total_est * 100
    if total_est > 0
    else 0
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Estudiantes", f"{total_est:,}")
kpi2.metric("Promedio General", f"{promedio:.1f}")
kpi3.metric("Tasa de Aprobacion", f"{tasa_aprob:.1f}%")
kpi4.metric("% en Riesgo Alto", f"{riesgo_alto:.1f}%", delta_color="inverse")

st.divider()

# -------------------------------------------------------------------------
# Visualizaciones
# -------------------------------------------------------------------------
st.markdown("### Visualizaciones Dinamicas")

viz1, viz2 = st.columns(2)
with viz1:
    st.markdown("**1. Distribucion de Calificaciones**")
    st.pyplot(plot_calificaciones(df_filt))

with viz2:
    st.markdown("**2. Puntaje Total por Departamento**")
    st.pyplot(plot_puntaje_por_departamento(df_filt))

viz3_col = st.columns(1)[0]
with viz3_col:
    st.markdown("**3. Indice de Riesgo por Calificacion**")
    st.pyplot(plot_riesgo_por_calificacion(df_filt))

viz4_col = st.columns(1)[0]
with viz4_col:
    st.markdown("**4. Horas de Sueño vs Puntaje Total (Bubble Chart)**")
    st.pyplot(plot_burbuja_estres_sueno(df_filt))

st.divider()

# -------------------------------------------------------------------------
# Tabla filtrada + descarga
# -------------------------------------------------------------------------
st.markdown("### Listado de Estudiantes Filtrados")
st.dataframe(df_filt, use_container_width=True, height=300)

csv_data = df_filt.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Descargar datos filtrados como CSV",
    data=csv_data,
    file_name="datos_filtrados_rendimiento.csv",
    mime="text/csv",
    key="download_csv",
)

# -------------------------------------------------------------------------
# Pie de pagina
# -------------------------------------------------------------------------
st.markdown(
    "---  \n"
    "*Dashboard TPI — Analisis de Datos | "
    "Tecnicatura Universitaria en Programacion — UTN*"
)

# 📊 TPI — Análisis de Rendimiento Académico

**Tecnicatura Universitaria en Programación — UTN**

Dashboard interactivo desarrollado con Streamlit para analizar el rendimiento académico de estudiantes.

## 🚀 Deploy

El dashboard está disponible online en:

**[👉 Abrir Dashboard en Streamlit Cloud](https://share.streamlit.io)**

> Deploy automático: cada push a `main` actualiza la app.

## 📁 Estructura del Proyecto

```
├── src/
│   ├── dashboard.py        # Dashboard Streamlit (entry point)
│   ├── etl.py              # Pipeline ETL (carga, limpieza, features)
│   ├── visualizaciones.py  # Gráficos estáticos (matplotlib/seaborn)
│   └── conexion.py         # Conexión a base de datos (opcional)
├── sql/
│   └── schema.sql          # Esquema de base de datos
├── graficos/               # Gráficos exportados (PNG)
├── Students_Performance_Dataset.csv   # Dataset crudo
├── requirements.txt        # Dependencias Python
└── .streamlit/
    └── config.toml         # Configuración del tema
```

## 🛠️ Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/TanoGS/Trabajo-Pr-ctico-Integrador---An-lisis-de-Datos.git
cd Trabajo-Pr-ctico-Integrador---An-lisis-de-Datos

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el dashboard
streamlit run src/dashboard.py
```

## 📊 Funcionalidades del Dashboard

- **KPIs en tiempo real**: Total de estudiantes, promedio general, tasa de aprobación, % en riesgo
- **Filtros interactivos**: Por departamento, género, nivel de ingreso, esfuerzo, calificación, asistencia y edad
- **Visualizaciones dinámicas**:
  - Distribución de calificaciones (A-F)
  - Puntaje total por departamento (boxplot)
  - Índice de riesgo por calificación
  - Relación horas de sueño vs puntaje (bubble chart)
- **Descarga de datos filtrados** en formato CSV

## 🧪 Pipeline ETL

El dashboard aplica el pipeline ETL internamente:

1. **Carga**: Lee el CSV crudo original
2. **Limpieza**: Remueve duplicados, normaliza strings, trata nulos
3. **Outliers**: Detección y tratamiento con método IQR
4. **Feature Engineering**: Crea columnas derivadas (calificación, puntaje total, índice de riesgo, etc.)

## 📌 Requisitos

- Python 3.9+
- streamlit
- pandas
- matplotlib
- seaborn

---

*UTN — Análisis de Datos — 2026*

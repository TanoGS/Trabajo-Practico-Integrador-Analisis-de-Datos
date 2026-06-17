import pandas as pd
import numpy as np


COLUMNAS_RENOMBRADAS = {
    "Student_ID": "student_id",
    "First_Name": "nombre",
    "Last_Name": "apellido",
    "Email": "email",
    "Gender": "genero",
    "Age": "edad",
    "Department": "departamento",
    "Attendance (%)": "asistencia",
    "Midterm_Score": "nota_parcial",
    "Final_Score": "nota_final",
    "Assignments_Avg": "promedio_tps",
    "Quizzes_Avg": "promedio_quizzes",
    "Participation_Score": "puntaje_participacion",
    "Projects_Score": "puntaje_proyectos",
    "Total_Score": "puntaje_total",
    "Grade": "calificacion",
    "Study_Hours_per_Week": "horas_estudio_semanal",
    "Extracurricular_Activities": "actividades_extra",
    "Internet_Access_at_Home": "acceso_internet",
    "Parent_Education_Level": "educacion_padres",
    "Family_Income_Level": "ingreso_familiar",
    "Stress_Level (1-10)": "nivel_estres",
    "Sleep_Hours_per_Night": "horas_sueno",
}

MAPEO_GENERO = {"Male": "Masculino", "Female": "Femenino"}
MAPEO_SINO = {"Yes": "Si", "No": "No"}
MAPEO_EDUCACION = {
    "High School": "Secundario",
    "Bachelor's": "Universitario",
    "Master's": "Maestria",
    "PhD": "Doctorado",
}
MAPEO_INGRESO = {"Low": "Bajo", "Medium": "Medio", "High": "Alto"}
MAPEO_DEPARTAMENTO = {
    "Business": "Negocios",
    "CS": "Computacion",
    "Engineering": "Ingenieria",
    "Mathematics": "Matematicas",
}

COLUMNAS_SCORES = [
    "nota_parcial",
    "nota_final",
    "promedio_tps",
    "promedio_quizzes",
    "puntaje_participacion",
    "puntaje_proyectos",
    "puntaje_total",
]


def cargar_csv(ruta):
    df = pd.read_csv(ruta)
    df = df.rename(columns=COLUMNAS_RENOMBRADAS)
    return df


def auditar(df):
    print(f"Registros: {len(df)}")
    print(f"Columnas: {len(df.columns)}")
    print(f"Duplicados: {df.duplicated().sum()}")
    print(f"IDs duplicados: {df['student_id'].duplicated().sum()}")
    print(f"\nNulos por columna:")
    nulos = df.isnull().sum()
    nulos_pos = nulos[nulos > 0]
    if len(nulos_pos) > 0:
        for col, count in nulos_pos.items():
            print(f"  {col}: {count} ({count / len(df) * 100:.1f}%)")
    else:
        print("  Sin valores nulos")
    print(f"\nTipos de datos:")
    print(df.dtypes)


def limpiar(df):
    df = df.copy()

    n_antes = len(df)
    df = df.drop_duplicates(subset=["student_id"]).reset_index(drop=True)
    print(f"Duplicados eliminados: {n_antes - len(df)}")

    df["nombre_completo"] = (
        df["nombre"].str.strip().str.title()
        + " "
        + df["apellido"].str.strip().str.title()
    )
    df = df.drop(columns=["nombre", "apellido", "email"])

    df["genero"] = df["genero"].str.strip().map(MAPEO_GENERO)
    df["departamento"] = df["departamento"].str.strip().map(MAPEO_DEPARTAMENTO)
    df["calificacion"] = df["calificacion"].str.strip().str.upper()
    df["actividades_extra"] = df["actividades_extra"].str.strip().map(MAPEO_SINO)
    df["acceso_internet"] = df["acceso_internet"].str.strip().map(MAPEO_SINO)
    df["educacion_padres"] = df["educacion_padres"].str.strip().map(MAPEO_EDUCACION)
    df["ingreso_familiar"] = df["ingreso_familiar"].str.strip().map(MAPEO_INGRESO)

    n_nulos_edu = df["educacion_padres"].isna().sum()
    if n_nulos_edu > 0:
        moda = df["educacion_padres"].mode()[0]
        df["educacion_padres"] = df["educacion_padres"].fillna(moda)
        print(f"Nulos en 'educacion_padres': {n_nulos_edu} imputados con moda ({moda})")

    cols_float = df.select_dtypes(include=["float64"]).columns
    df[cols_float] = df[cols_float].round(2)

    cols_inicio = ["student_id", "nombre_completo", "genero", "edad", "departamento"]
    cols_resto = [c for c in df.columns if c not in cols_inicio]
    df = df[cols_inicio + cols_resto]

    print(f"Registros finales: {len(df)}")
    print(f"Nulos restantes: {df.isnull().sum().sum()}")
    return df


def detectar_outliers_iqr(serie):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    return (serie < lim_inf) | (serie > lim_sup), lim_inf, lim_sup


def tratar_outliers(df, columnas):
    df = df.copy()
    resumen = []
    for col in columnas:
        mask, lim_inf, lim_sup = detectar_outliers_iqr(df[col])
        n = mask.sum()
        if n > 0:
            df.loc[df[col] < lim_inf, col] = round(lim_inf, 2)
            df.loc[df[col] > lim_sup, col] = round(lim_sup, 2)
        resumen.append(
            {
                "columna": col,
                "outliers": n,
                "limite_inferior": round(lim_inf, 2),
                "limite_superior": round(lim_sup, 2),
            }
        )
        print(f"  {col}: {n} outliers | rango IQR [{lim_inf:.2f}, {lim_sup:.2f}]")
    return df, pd.DataFrame(resumen)


def _normalizar(serie, invertir=False):
    rango = serie.max() - serie.min()
    if rango == 0:
        return pd.Series(0.5, index=serie.index)
    norm = (serie - serie.min()) / rango
    return (1 - norm) if invertir else norm


def crear_features(df):
    df = df.copy()

    df["promedio_continuo"] = (
        (df["promedio_tps"] + df["promedio_quizzes"] + df["puntaje_proyectos"]) / 3
    ).round(2)

    df["promedio_examenes"] = (
        (df["nota_parcial"] + df["nota_final"]) / 2
    ).round(2)

    df["brecha_evaluacion"] = (
        df["promedio_continuo"] - df["promedio_examenes"]
    ).round(2)

    df["indice_riesgo"] = (
        _normalizar(df["asistencia"], invertir=True) * 30
        + _normalizar(df["nivel_estres"]) * 20
        + _normalizar(df["horas_sueno"], invertir=True) * 20
        + _normalizar(df["horas_estudio_semanal"], invertir=True) * 30
    ).round(2)

    puntaje_esfuerzo = (
        _normalizar(df["horas_estudio_semanal"]) * 40
        + _normalizar(df["puntaje_participacion"]) * 30
        + (df["actividades_extra"] == "Si").astype(int) * 30
    )
    df["categoria_esfuerzo"] = pd.cut(
        puntaje_esfuerzo,
        bins=[-np.inf, 33, 66, np.inf],
        labels=["Bajo", "Medio", "Alto"],
    )

    puntaje_bienestar = (
        _normalizar(df["nivel_estres"], invertir=True) * 50
        + _normalizar(df["horas_sueno"]) * 50
    )
    df["categoria_bienestar"] = pd.cut(
        puntaje_bienestar,
        bins=[-np.inf, 33, 66, np.inf],
        labels=["Bajo", "Medio", "Alto"],
    )

    print("Features creados:")
    print("  - promedio_continuo (TPs + Quizzes + Proyectos / 3)")
    print("  - promedio_examenes (Parcial + Final / 2)")
    print("  - brecha_evaluacion (Continuo - Examenes)")
    print("  - indice_riesgo (0-100, compuesto de asistencia, estres, sueno, estudio)")
    print("  - categoria_esfuerzo (Bajo / Medio / Alto)")
    print("  - categoria_bienestar (Bajo / Medio / Alto)")
    return df

import os

import matplotlib.pyplot as plt
import seaborn as sns

DIRECTORIO_GRAFICOS = "graficos"


def configurar_estilo():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update(
        {
            "figure.figsize": (12, 6),
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "font.size": 10,
            "figure.dpi": 100,
        }
    )


def _guardar(fig, nombre):
    os.makedirs(DIRECTORIO_GRAFICOS, exist_ok=True)
    fig.savefig(
        os.path.join(DIRECTORIO_GRAFICOS, f"{nombre}.png"),
        dpi=150,
        bbox_inches="tight",
    )


def heatmap_correlacion(df):
    columnas = [
        "asistencia",
        "nota_parcial",
        "nota_final",
        "promedio_tps",
        "promedio_quizzes",
        "puntaje_participacion",
        "puntaje_proyectos",
        "puntaje_total",
        "horas_estudio_semanal",
        "nivel_estres",
        "horas_sueno",
        "indice_riesgo",
    ]
    corr = df[columnas].corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        linewidths=0.5,
        square=True,
        ax=ax,
        cbar_kws={"label": "Coeficiente de Correlacion"},
    )
    ax.set_title("Matriz de Correlacion — Variables Academicas y Comportamentales")
    plt.tight_layout()
    _guardar(fig, "01_correlacion")
    plt.show()


def boxplot_riesgo_calificacion(df):
    orden = ["A", "B", "C", "D", "F"]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=df,
        x="calificacion",
        y="indice_riesgo",
        hue="calificacion",
        order=orden,
        palette="RdYlGn_r",
        legend=False,
        ax=ax,
    )
    ax.set_title("Distribucion del Indice de Riesgo por Calificacion")
    ax.set_xlabel("Calificacion")
    ax.set_ylabel("Indice de Riesgo (0-100)")
    plt.tight_layout()
    _guardar(fig, "02_riesgo_calificacion")
    plt.show()


def barras_ingreso_esfuerzo(df):
    orden_ingreso = ["Bajo", "Medio", "Alto"]
    orden_esfuerzo = ["Bajo", "Medio", "Alto"]

    resumen = (
        df.groupby(["ingreso_familiar", "categoria_esfuerzo"], observed=True)[
            "puntaje_total"
        ]
        .mean()
        .reset_index()
    )

    pivot = resumen.pivot(
        index="ingreso_familiar",
        columns="categoria_esfuerzo",
        values="puntaje_total",
    ).reindex(orden_ingreso)[orden_esfuerzo]

    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind="bar", ax=ax, width=0.7, edgecolor="black", linewidth=0.5)
    ax.set_title("Puntaje Total Promedio por Ingreso Familiar y Nivel de Esfuerzo")
    ax.set_xlabel("Nivel de Ingreso Familiar")
    ax.set_ylabel("Puntaje Total Promedio")
    ax.legend(title="Esfuerzo")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    _guardar(fig, "03_ingreso_esfuerzo")
    plt.show()


def scatter_brecha_estres(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(
        data=df,
        x="nivel_estres",
        y="brecha_evaluacion",
        hue="departamento",
        alpha=0.4,
        ax=ax,
        s=30,
    )
    sns.regplot(
        data=df,
        x="nivel_estres",
        y="brecha_evaluacion",
        scatter=False,
        color="black",
        line_kws={"linewidth": 2},
        ax=ax,
    )
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_title("Brecha de Evaluacion vs Nivel de Estres por Departamento")
    ax.set_xlabel("Nivel de Estres (1-10)")
    ax.set_ylabel("Brecha de Evaluacion (Continuo - Examenes)")
    ax.legend(title="Departamento", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    _guardar(fig, "04_brecha_estres")
    plt.show()


def burbuja_estres_sueno(df):
    """Grafico 5: Bubble plot — Horas de sueno vs Puntaje total,
    tamano de burbuja = nivel de estres, color = departamento.
    Relacion de estres y sueno con el rendimiento academico.
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.scatterplot(
        data=df,
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
        data=df,
        x="horas_sueno",
        y="puntaje_total",
        scatter=False,
        color="black",
        line_kws={"linewidth": 2, "linestyle": "--"},
        ax=ax,
    )
    ax.set_title("Horas de Sueno vs Puntaje Total — Tamano segun Nivel de Estres")
    ax.set_xlabel("Horas de Sueno por Noche")
    ax.set_ylabel("Puntaje Total")
    ax.legend(title="Departamento / Estres", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    _guardar(fig, "05_estres_sueno")
    plt.show()

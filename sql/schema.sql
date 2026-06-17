-- TPI: Analisis de Rendimiento Academico
-- Esquema de base de datos para MySQL

CREATE DATABASE IF NOT EXISTS tpi_rendimiento_academico;
USE tpi_rendimiento_academico;

-- Tabla de datos crudos (carga directa del CSV)
DROP TABLE IF EXISTS rendimiento_crudo;
CREATE TABLE rendimiento_crudo (
    student_id VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100),
    genero VARCHAR(20),
    edad INT,
    departamento VARCHAR(50),
    asistencia DECIMAL(5,2),
    nota_parcial DECIMAL(5,2),
    nota_final DECIMAL(5,2),
    promedio_tps DECIMAL(5,2),
    promedio_quizzes DECIMAL(5,2),
    puntaje_participacion DECIMAL(5,2),
    puntaje_proyectos DECIMAL(5,2),
    puntaje_total DECIMAL(5,2),
    calificacion CHAR(1),
    horas_estudio_semanal DECIMAL(4,1),
    actividades_extra VARCHAR(3),
    acceso_internet VARCHAR(3),
    educacion_padres VARCHAR(30),
    ingreso_familiar VARCHAR(10),
    nivel_estres INT,
    horas_sueno DECIMAL(3,1)
);

-- Tabla de datos limpios con variables derivadas
DROP TABLE IF EXISTS rendimiento_limpio;
CREATE TABLE rendimiento_limpio (
    student_id VARCHAR(10) PRIMARY KEY,
    nombre_completo VARCHAR(100),
    genero VARCHAR(20),
    edad INT,
    departamento VARCHAR(50),
    asistencia DECIMAL(5,2),
    nota_parcial DECIMAL(5,2),
    nota_final DECIMAL(5,2),
    promedio_tps DECIMAL(5,2),
    promedio_quizzes DECIMAL(5,2),
    puntaje_participacion DECIMAL(5,2),
    puntaje_proyectos DECIMAL(5,2),
    puntaje_total DECIMAL(5,2),
    calificacion CHAR(1),
    horas_estudio_semanal DECIMAL(4,1),
    actividades_extra VARCHAR(2),
    acceso_internet VARCHAR(2),
    educacion_padres VARCHAR(30),
    ingreso_familiar VARCHAR(10),
    nivel_estres INT,
    horas_sueno DECIMAL(3,1),
    promedio_continuo DECIMAL(5,2),
    promedio_examenes DECIMAL(5,2),
    brecha_evaluacion DECIMAL(6,2),
    indice_riesgo DECIMAL(5,2),
    categoria_esfuerzo VARCHAR(10),
    categoria_bienestar VARCHAR(10)
);

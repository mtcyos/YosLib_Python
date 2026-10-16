-- -*- coding: utf-8 -*-
-- Estructura corregida para SQLite y portátil para el futuro
CREATE TABLE IF NOT EXISTS FncHlp (
    NumReg INTEGER PRIMARY KEY AUTOINCREMENT,  -- Tu clave primaria e interna inmutable
    cFun VARCHAR(100),                         -- Nombre de la función
    cTit VARCHAR(255),                         -- Título (Primer comentario '#' bajo la def)
    cDes TEXT,                                 -- Descripción extensa de la ayuda (Manual)
    cPmt TEXT,                                 -- Diccionario extendido y variables de parámetros
    cObs TEXT,                                 -- Observaciones de mantenimiento o enlaces
    cOri VARCHAR(100),                         -- Origen del código: 'Yos_Txt.py' o 'YosLib.FncDef'
    cEst VARCHAR(3),                           -- Estado: '', 'Nue', 'Eli'
    cModRegNik VARCHAR(20),                    -- Nick del último en modificar ('mtcyos' o 'Bin')
    cModRegTim VARCHAR(20),                    -- Timestamp unificado "AAAAmmmddd HH:mm:ss"
    UNIQUE (cOri, cFun)                        -- ¡SOLUCIÓN! Evita que se duplique la función por origen
);

-- -*- coding: utf-8 -*-
-- Estructura compatible y portable para FncDef
CREATE TABLE IF NOT EXISTS FncDef (
    NumReg INTEGER PRIMARY KEY AUTOINCREMENT,
    cFnc VARCHAR(100),                         -- Nombre de la función virtual
    cCmd TEXT,                                 -- Código puro de Python (Bloque de texto libre)
    cModRegNik VARCHAR(20),                    -- Tu estándar de Nick para control
    cModRegTim VARCHAR(20),                    -- Tu estándar de fecha unificada "AAAAmmmddd HH:mm:ss"
);


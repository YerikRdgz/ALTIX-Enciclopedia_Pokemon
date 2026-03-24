CREATE DATABASE  Enciclopedia_Pokemon;
USE Enciclopedia_Pokemon;

-- Tabla de Tipos
CREATE TABLE Tipos (
    id_tipo INT PRIMARY KEY AUTO_INCREMENT,
    nombre_tipo VARCHAR(50) NOT NULL
);

-- Tabla de Habilidades
CREATE TABLE Habilidades (
    id_habilidad INT PRIMARY KEY AUTO_INCREMENT,
    nombre_habilidad VARCHAR(100) NOT NULL
);

-- Tabla de Pokémon
CREATE TABLE Pokemon (
    id_pokemon INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    altura FLOAT,
    peso FLOAT,
    ratio_captura FLOAT,
    es_legendario BOOLEAN,
    generacion INT
);

-- Relación Pokémon - Tipos
CREATE TABLE Pokemon_Tipos (
    id_pokemon INT,
    id_tipo INT,
    es_tipo_principal BOOLEAN,
    PRIMARY KEY (id_pokemon, id_tipo),
    FOREIGN KEY (id_pokemon) REFERENCES Pokemon(id_pokemon),
    FOREIGN KEY (id_tipo) REFERENCES Tipos(id_tipo)
);

-- Relación Pokémon - Habilidades
CREATE TABLE Pokemon_Habilidades (
    id_pokemon INT,
    id_habilidad INT,
    PRIMARY KEY (id_pokemon, id_habilidad),
    FOREIGN KEY (id_pokemon) REFERENCES Pokemon(id_pokemon),
    FOREIGN KEY (id_habilidad) REFERENCES Habilidades(id_habilidad)
);

-- Tabla de Estadísticas Base
CREATE TABLE Estadisticas_Base (
    id_pokemon INT PRIMARY KEY,
    ps INT,
    ataque INT,
    defensa INT,
    ataque_especial INT,
    defensa_especial INT,
    velocidad INT,
    total_estadisticas INT,
    FOREIGN KEY (id_pokemon) REFERENCES Pokemon(id_pokemon)
);

-- Tabla de Efectividad de Combate
CREATE TABLE Efectividad_Combate (
    id_pokemon INT,
    id_tipo_ataque INT,
    multiplicador FLOAT,
    PRIMARY KEY (id_pokemon, id_tipo_ataque),
    FOREIGN KEY (id_pokemon) REFERENCES Pokemon(id_pokemon),
    FOREIGN KEY (id_tipo_ataque) REFERENCES Tipos(id_tipo)
);
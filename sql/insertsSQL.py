import pandas as pd
from sqlalchemy import create_engine

# --- NORMALIZACIÓN Y CARGA A MYSQL

try:
    datos = pd.read_csv("datos/pokemon_final.csv")
except FileNotFoundError:
    print("Error: Ejecuta primero lista_pokemon.py")
    exit()

# --- A. Catálogos ---

# 1. Tipos
tipos_1 = datos["Tipo 1"].dropna().astype(str)
tipos_2 = datos["Tipo 2"].dropna().astype(str)

todos_tipos = set(tipos_1) | set(tipos_2)

# Descartamos cualquier valor que signifique "vacío"
for basura in ["None", "nan", "Nan", ""]:
    todos_tipos.discard(basura)

df_tipos = pd.DataFrame(
    {
        "id_tipo": range(1, len(todos_tipos) + 1),
        "nombre_tipo": sorted(list(todos_tipos)),
    }
)
map_tipos = dict(zip(df_tipos["nombre_tipo"], df_tipos["id_tipo"]))

# 2. Habilidades
todas_habs = set(
    h.strip()
    for lista in datos["Habilidades"].dropna().astype(str)
    for h in lista.split(",")
)

# Descartamos nulos en las habilidades
for basura in ["None", "nan", "Nan", ""]:
    todas_habs.discard(basura)

df_habilidades = pd.DataFrame(
    {
        "id_habilidad": range(1, len(todas_habs) + 1),
        "nombre_habilidad": sorted(list(todas_habs)),
    }
)
map_habs = dict(zip(df_habilidades["nombre_habilidad"], df_habilidades["id_habilidad"]))

# --- B. Entidades Principales ---
df_pokemon = datos[
    [
        "id_pokemon",
        "Nombre",
        "altura",
        "peso",
        "ratio_captura",
        "es_legendario",
        "generacion",
    ]
].copy()
df_stats = datos[
    [
        "id_pokemon",
        "PS",
        "Ataque",
        "Defensa",
        "ataque_especial",
        "defensa_especial",
        "Velocidad",
        "total_estadisticas",
    ]
].copy()
# Ajustamos los nombres a minúsculas
df_stats.columns = [
    "id_pokemon",
    "ps",
    "ataque",
    "defensa",
    "ataque_especial",
    "defensa_especial",
    "velocidad",
    "total_estadisticas",
]

# --- C. Tablas Intermedias ---
poke_tipos_data, poke_habs_data = [], []

for _, row in datos.iterrows():
    p_id = row["id_pokemon"]

    if row["Tipo 1"] in map_tipos:
        poke_tipos_data.append(
            {
                "id_pokemon": p_id,
                "id_tipo": map_tipos[row["Tipo 1"]],
                "es_tipo_principal": 1,
            }
        )
    if row["Tipo 2"] in map_tipos:
        poke_tipos_data.append(
            {
                "id_pokemon": p_id,
                "id_tipo": map_tipos[row["Tipo 2"]],
                "es_tipo_principal": 0,
            }
        )

    if pd.notna(row["Habilidades"]):
        for h in str(row["Habilidades"]).split(","):
            if h.strip() in map_habs:
                poke_habs_data.append(
                    {"id_pokemon": p_id, "id_habilidad": map_habs[h.strip()]}
                )

df_pokemon_tipos = pd.DataFrame(poke_tipos_data)
df_pokemon_habilidades = pd.DataFrame(poke_habs_data)

# --- D. Efectividad de Combate ---
cols_resistencia = [c for c in datos.columns if "Resistance vs" in c]
df_efectividad_raw = datos.melt(
    id_vars=["id_pokemon"],
    value_vars=cols_resistencia,
    var_name="tipo_ataque",
    value_name="multiplicador",
)

# Extraer solo el tipo y mapearlo al ID
df_efectividad_raw["tipo_ataque"] = df_efectividad_raw["tipo_ataque"].str.replace(
    "Resistance vs ", ""
)
df_efectividad_raw["id_tipo_ataque"] = df_efectividad_raw["tipo_ataque"].map(map_tipos)

df_efectividad = df_efectividad_raw[
    ["id_pokemon", "id_tipo_ataque", "multiplicador"]
].dropna()
df_efectividad.columns = ["id_pokemon", "id_tipo_ataque", "multiplicador"]
df_efectividad["id_tipo_ataque"] = df_efectividad["id_tipo_ataque"].astype(int)


# 3. Eliminando duplicados

# Borramos Pokémon repetidos por su número de Pokedex
df_pokemon.drop_duplicates(subset=["id_pokemon"], keep="first", inplace=True)
df_stats.drop_duplicates(subset=["id_pokemon"], keep="first", inplace=True)

# Borramos combinaciones repetidas en las tablas
df_pokemon_tipos.drop_duplicates(subset=["id_pokemon", "id_tipo"], inplace=True)
df_pokemon_habilidades.drop_duplicates(
    subset=["id_pokemon", "id_habilidad"], inplace=True
)
df_efectividad.drop_duplicates(subset=["id_pokemon", "id_tipo_ataque"], inplace=True)

# 4. CONEXIÓN E INSERCIÓN A MYSQL

# RECUERDA: Verificar "root:password"
cadena_conexion = "mysql+pymysql://root:password@localhost:3306/Enciclopedia_Pokemon"

try:
    engine = create_engine(cadena_conexion)

    # Escribimos los nombres en MINÚSCULAS para evitar los UserWarnings de Pandas
    df_tipos.to_sql("tipos", con=engine, if_exists="append", index=False)
    df_habilidades.to_sql("habilidades", con=engine, if_exists="append", index=False)

    df_pokemon.to_sql("pokemon", con=engine, if_exists="append", index=False)
    df_stats.to_sql("estadisticas_base", con=engine, if_exists="append", index=False)

    df_pokemon_tipos.to_sql(
        "pokemon_tipos", con=engine, if_exists="append", index=False
    )
    df_pokemon_habilidades.to_sql(
        "pokemon_habilidades", con=engine, if_exists="append", index=False
    )
    df_efectividad.to_sql(
        "efectividad_combate", con=engine, if_exists="append", index=False
    )

    print("EXITO TOTAL")
except Exception as e:
    print(f"Error al conectar con MySQL: {e}")

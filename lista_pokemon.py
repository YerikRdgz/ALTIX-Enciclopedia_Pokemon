import pandas as pd

# --- EXTRACCIÓN Y LIMPIEZA ---

try:
    datos = pd.read_csv("pokemon.csv")
except FileNotFoundError:
    print("Error: No se encontró 'pokemon.csv'")
    exit()

# 1. Eliminar columnas que no sirven
cols_a_borrar = [
    "nombre_japones",
    "clasificacion",
    "pasos_base_para_eclosion",
    "felicidad_base",
    "crecimiento_experiencia",
    "%_macho",
]
datos.drop(columns=cols_a_borrar, inplace=True, errors="ignore")

# 2. Renombrar las columnas principales al formato de MySQL
columnas_map = {
    "No_Pokedex": "id_pokemon",
    "nombre": "Nombre",
    "habilidades": "Habilidades",
    "tipo1": "Tipo 1",
    "tipo2": "Tipo 2",
    "ataque": "Ataque",
    "defensa": "Defensa",
    "velocidad": "Velocidad",
    "ataque_especial": "ataque_especial",
    "defensa_especial": "defensa_especial",
    "Puntos_de_salud": "PS",
    "total_base": "total_estadisticas",
    "altura_(m)": "altura",
    "peso_(kg)": "peso",
    "Probabilidad_de_captura": "ratio_captura",
}
datos.rename(columns=columnas_map, inplace=True)

# 3. Limpieza Matemática
datos["ratio_captura"] = (
    datos["ratio_captura"].astype(str).str.extract(r"(\d+)").astype(float)
)
datos["altura"] = datos["altura"].fillna(0)
datos["peso"] = datos["peso"].fillna(0)


# 4. Limpiar Habilidades
def limpiar_habilidades(valor):
    if pd.isna(valor) or valor == "":
        return ""
    for char in "[]'\"":
        valor = str(valor).replace(char, "")
    lista = [h.strip().title() for h in valor.split(",")]
    return ", ".join(lista)


datos["Habilidades"] = datos["Habilidades"].apply(limpiar_habilidades)

# 5. Estandarizar Tipos al Inglés con mayúsculas
datos["Tipo 1"] = datos["Tipo 1"].dropna().str.title()
datos["Tipo 2"] = datos["Tipo 2"].fillna("None").str.title()

# 6. Estandarizar columnas de resistencia al inglés
map_es_a_en = {
    "planta": "Grass",
    "fuego": "Fire",
    "agua": "Water",
    "insecto": "Bug",
    "siniestro": "Dark",
    "dragon": "Dragon",
    "electrico": "Electric",
    "hada": "Fairy",
    "lucha": "Fighting",
    "volador": "Flying",
    "fantasma": "Ghost",
    "tierra": "Ground",
    "hielo": "Ice",
    "normal": "Normal",
    "veneno": "Poison",
    "psiquico": "Psychic",
    "roca": "Rock",
    "acero": "Steel",
}

for col in datos.columns:
    if "contraataque_" in col:
        tipo_es = col.replace("contraataque_", "").strip()
        tipo_en = map_es_a_en.get(tipo_es, tipo_es.title())
        datos.rename(columns={col: f"Resistance vs {tipo_en}"}, inplace=True)

# 7. Guardar el archivo inmaculado
datos.to_csv("pokemon_final.csv", index=False, encoding="utf-8")
print("Limpieza completada")

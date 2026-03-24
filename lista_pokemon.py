import pandas as pd

# 1. Cargar el archivo original
try:
    # Cambia 'pokemon.csv' por el nombre exacto de tu archivo si es distinto
    datos = pd.read_csv('pokemon.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo 'pokemon.csv'")
    exit()

# --- DICCIONARIOS MAESTROS ---

tipos_es = {
    'grass': 'Planta', 'fire': 'Fuego', 'water': 'Agua', 'bug': 'Bicho',
    'normal': 'Normal', 'poison': 'Veneno', 'electric': 'Eléctrico',
    'ground': 'Tierra', 'fairy': 'Hada', 'fighting': 'Lucha',
    'psychic': 'Psíquico', 'rock': 'Roca', 'ghost': 'Fantasma',
    'ice': 'Hielo', 'dragon': 'Dragón', 'dark': 'Siniestro',
    'steel': 'Acero', 'flying': 'Volador'
}

habilidades_es = {
    'Overgrow': 'Espesura', 'Chlorophyll': 'Clorofila', 'Blaze': 'Mar Llamas', 
    'Torrent': 'Torrente', 'Shield Dust': 'Polvo Escudo', 'Shed Skin': 'Mudar', 
    'Compoundeyes': 'Ojo Compuesto', 'Compound Eyes': 'Ojo Compuesto', 'Swarm': 'Enjambre', 
    'Keen Eye': 'Vista Lince', 'Tangled Feet': 'Tanteo', 'Guts': 'Agallas', 
    'Intimidate': 'Intimidación', 'Static': 'Electricidad Estática', 'Levitate': 'Levitación', 
    'Rain Dish': 'Cura Lluvia', 'Early Bird': 'Madrugar', 'Insomnia': 'Insomnio', 
    'Run Away': 'Fuga', 'Sniper': 'Francotirador', 'Big Pecks': 'Sacapecho',
    'Sturdy': 'Robustez', 'Damp': 'Humedad', 'Limber': 'Flexibilidad', 'Sand Veil': 'Velo Arena',
    'Beast Boost': 'Ultraimpulso', 'Tinted Lens': 'Cromolente', 'Natural Cure': 'Cura Natural'
}


def traducir_habilidades(valor):
    if pd.isna(valor) or valor == "": return ""
    # Quitar corchetes y comillas: de "['Blaze']" a "Blaze"
    if isinstance(valor, str):
        for char in "[]'\"":
            valor = valor.replace(char, "")
        lista = [h.strip() for h in valor.split(',')]
    else:
        lista = [str(valor).strip()]
    
    # Traducir cada una. Si no está en el diccionario, se pone la primera en mayúscula.
    traducidas = [habilidades_es.get(h, h).title() for h in lista if h]
    return ", ".join(traducidas)

# --- PROCESAMIENTO ---

# 1. Renombrar columnas base (si existen en tu archivo)
columnas_map = {
    'nombre': 'Nombre', 'habilidades': 'Habilidades', 'abilities': 'Habilidades',
    'tipo1': 'Tipo 1', 'type1': 'Tipo 1', 'tipo2': 'Tipo 2', 'type2': 'Tipo 2',
    'ataque': 'Ataque', 'defensa': 'Defensa', 'velocidad': 'Velocidad',
    'puntos_de_salud': 'PS', 'hp': 'PS'
}
datos.rename(columns=columnas_map, inplace=True)

# 2. Traducir Habilidades (Limpieza 100%)
if 'Habilidades' in datos.columns:
    datos['Habilidades'] = datos['Habilidades'].apply(traducir_habilidades)

# 3. Traducir Tipos
for col in ['Tipo 1', 'Tipo 2']:
    if col in datos.columns:
        datos[col] = datos[col].astype(str).str.lower().str.strip().map(tipos_es).fillna(datos[col])

# 4. Traducir columnas de "contraataque" o "against"
for col in datos.columns:
    if 'contraataque_' in col.lower() or 'against_' in col.lower():
        # Extraer el tipo (ej: de contraataque_fuego saca "fuego")
        tipo_en = col.lower().replace('contraataque_', '').replace('against_', '').strip()
        # Traducir el tipo para el encabezado
        tipo_es_header = tipos_es.get(tipo_en, tipo_en.title())
        datos.rename(columns={col: f'Resistencia vs {tipo_es_header}'}, inplace=True)

# 5. ELIMINAR COLUMNA JAPONESA DEFINITIVAMENTE
# Busca cualquier columna que contenga "jap" o "japanese"
cols_jap = [c for c in datos.columns if 'jap' in c.lower() or 'japanese' in c.lower()]
datos.drop(columns=cols_jap, inplace=True, errors='ignore')

# 6. Guardar el archivo final perfecto
# utf-8-sig es para que Excel abra bien las tildes y eñes
datos.to_csv('pokemon_final_1.csv', index=False, encoding='utf-8-sig')

print("¡Hecho! Archivo 'pokemon_final_perfecto.csv' generado.")
print(f"Se eliminaron las columnas: {cols_jap}")
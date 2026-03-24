import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd

# 1. CONEXIÓN A MYSQL
try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",  # <-- Tu usuario
        password="password",  # <-- Tu contraseña
        database="Enciclopedia_Pokemon",
    )
    print("Conexión exitosa a la base de datos MySQL.")
except Exception as e:
    print(f"Error conectando a MySQL: {e}")
    exit()

colores_pokemon = {
    "NORMAL": "#A8A878",
    "FIRE": "#F08030",
    "WATER": "#6890F0",
    "ELECTR": "#F8D030",  # Electric
    "GRASS": "#78C850",
    "ICE": "#98D8D8",
    "FIGHT": "#C03028",  # Fighting
    "POISON": "#A040A0",
    "GROUND": "#E0C068",
    "FLYING": "#A890F0",
    "PSYCHC": "#F85888",  # Psychic
    "BUG": "#A8B820",
    "ROCK": "#B8A038",
    "GHOST": "#705898",
    "DRAGON": "#7038F8",
    "DARK": "#705848",
    "STEEL": "#B8B8D0",
    "FAIRY": "#EE99AC",
}

# GRÁFICA 1: TOP 10 MEJORES POKÉMON
query_top10 = """
    SELECT p.nombre, t.nombre_tipo AS tipo1, e.total_estadisticas
    FROM pokemon p
    JOIN estadisticas_base e ON p.id_pokemon = e.id_pokemon
    JOIN pokemon_tipos pt ON p.id_pokemon = pt.id_pokemon AND pt.es_tipo_principal = 1
    JOIN tipos t ON pt.id_tipo = t.id_tipo
    ORDER BY e.total_estadisticas DESC
    LIMIT 10;
"""
df_top10 = pd.read_sql(query_top10, conexion)

fig, ax = plt.subplots(figsize=(10, 6))
tipos_unicos = df_top10["tipo1"].unique()
colores = [colores_pokemon.get(tipo.upper(), "#CCCCCC") for tipo in tipos_unicos]
color_map = dict(zip(tipos_unicos, colores))
bar_colors = df_top10["tipo1"].map(color_map)

ax.barh(
    df_top10["nombre"][::-1],
    df_top10["total_estadisticas"][::-1],
    color=bar_colors[::-1],
)

legend_patches = [mpatches.Patch(color=color_map[t], label=t) for t in tipos_unicos]
ax.legend(
    handles=legend_patches,
    title="Tipo",
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)

ax.set_xlabel("Total Estadisticas")
ax.set_title("Top 10 Mejores Pokémon")
ax.set_xlim(600, 800)
plt.tight_layout()
plt.savefig("grafica1_top10.png")
plt.close()

# GRÁFICA 2: MÁS DIFÍCILES DE CAPTURAR
query_captura = """
    SELECT p.nombre, p.ratio_captura, p.es_legendario, e.total_estadisticas
    FROM pokemon p
    JOIN estadisticas_base e ON p.id_pokemon = e.id_pokemon
    ORDER BY p.ratio_captura ASC, e.total_estadisticas DESC
    LIMIT 10;
"""
df_hardest = pd.read_sql(query_captura, conexion)

fig, ax = plt.subplots(figsize=(10, 6))
legendario_colors = df_hardest["es_legendario"].map({1: "limegreen", 0: "crimson"})

ax.barh(
    df_hardest["nombre"][::-1],
    df_hardest["ratio_captura"][::-1],
    color=legendario_colors[::-1],
)

leg_patches2 = [
    mpatches.Patch(color="limegreen", label="Legendario (Si)"),
    mpatches.Patch(color="crimson", label="Legendario (No)"),
]
ax.legend(handles=leg_patches2, title="Es Legendario", loc="lower right")

ax.set_xlabel("Ratio de captura")
ax.set_title("Top 10 Pokémon Más Difíciles de Capturar")
plt.tight_layout()
plt.savefig("grafica2_captura.png")
plt.close()

# GRÁFICA 3: MAPA DE CALOR
query_heatmap = """
    SELECT p.nombre, t.nombre_tipo AS tipo_ataque, ec.multiplicador
    FROM efectividad_combate ec
    JOIN pokemon p ON ec.id_pokemon = p.id_pokemon
    JOIN tipos t ON ec.id_tipo_ataque = t.id_tipo
    JOIN (
        SELECT id_pokemon FROM estadisticas_base ORDER BY total_estadisticas DESC LIMIT 10
    ) top10 ON p.id_pokemon = top10.id_pokemon;
"""
df_efectividad = pd.read_sql(query_heatmap, conexion)

heatmap_data = df_efectividad.pivot(
    index="nombre", columns="tipo_ataque", values="multiplicador"
)

fig, ax = plt.subplots(figsize=(14, 8))
cax = ax.imshow(heatmap_data.values, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=2)
cbar = fig.colorbar(cax, ax=ax)
cbar.set_label("Damage Multiplier (Red = Weakness, Green = Resistance)")

ax.set_xticks(np.arange(len(heatmap_data.columns)))
ax.set_yticks(np.arange(len(heatmap_data.index)))
ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")
ax.set_yticklabels(heatmap_data.index)

for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        val = heatmap_data.values[i, j]
        text_color = "white" if (val >= 2.0 or val <= 0.25) else "black"
        ax.text(
            j,
            i,
            f"{val:.2g}",
            ha="center",
            va="center",
            color=text_color,
            fontweight="bold",
        )

ax.set_title("Fortalezas y Debilidades de los Top 10 Mejores Pokémon")
fig.tight_layout()
plt.savefig("grafica3_heatmap.png")
plt.close()

# GRÁFICA 4: EQUIPO ESTRATÉGICO VS REGIGIGAS
query_equipo = """
    SELECT p.nombre, t.nombre_tipo AS tipo1
    FROM pokemon p
    JOIN pokemon_tipos pt ON p.id_pokemon = pt.id_pokemon AND pt.es_tipo_principal = 1
    JOIN tipos t ON pt.id_tipo = t.id_tipo
    WHERE p.nombre IN ('Lucario', 'Gengar', 'Machamp', 'Buzzwole');
"""
df_equipo = pd.read_sql(query_equipo, conexion)

probabilidades = {"Gengar": 95, "Lucario": 85, "Buzzwole": 80, "Machamp": 75}
df_equipo["probabilidad_victoria"] = df_equipo["nombre"].map(probabilidades)

fig, ax = plt.subplots(figsize=(10, 6))

# --- CORRECCIÓN DE COLORES AQUÍ ---
tipos_equipo = df_equipo["tipo1"].unique()

# Creamos un diccionario exclusivo para los tipos de este equipo
color_map_eq = {
    tipo: colores_pokemon.get(tipo.upper(), "#CCCCCC") for tipo in tipos_equipo
}

# Mapeamos los colores directamente a la columna del dataframe
bar_colors_eq = df_equipo["tipo1"].map(color_map_eq)
# ----------------------------------

bars = ax.bar(
    df_equipo["nombre"], df_equipo["probabilidad_victoria"], color=bar_colors_eq
)

# La leyenda se arma usando nuestro nuevo diccionario corregido
import matplotlib.patches as mpatches  # Por si no lo tenías importado

leg_patches_eq = [mpatches.Patch(color=color_map_eq[t], label=t) for t in tipos_equipo]
ax.legend(handles=leg_patches_eq, title="Tipo", loc="upper right")

for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 1,
        f"{int(yval)}%",
        ha="center",
        va="bottom",
        fontweight="bold",
        fontsize=12,
    )

ax.set_ylabel("Probabilidad de Victoria (%)")
ax.set_title("Equipo Estratégico vs Regigigas")
ax.set_ylim(0, 105)

plt.tight_layout()
plt.savefig("grafica4_equipo.png")
plt.close()

# **ALTIX: Análisis de Visualizaciones de Datos Pokémon**

Este documento detalla la interpretación de las cuatro gráficas generadas para el cliente, extraídas de nuestra base de datos MySQL.

## **Gráfica 1: Top 10 de los Mejores Pokémon Agrupados por Tipo**

Esta visualización de barras identifica a los Pokémon más sobresalientes de la base de datos basándose en la suma total de sus estadísticas base.

* Agruparlos por su tipo principal permite identificar rápidamente qué categorías elementales dominan el panorama competitivo. Se observa una tendencia clara donde los tipos Dragón, Acero y Psíquico suelen tener a los representantes con los valores más altos.

## **Gráfica 2: Top 10 de los Pokémon Más Difíciles de Capturar**

Esta gráfica detalla las especies que presentan el mayor desafío de captura.

* La dificultad de captura no es aleatoria, sino que obedece a un valor matemático oculto en la programación del juego conocido como el "Catch Rate" (Ratio de Captura). Este valor oscila entre 3 y 255\.  
* Los Pokémon que aparecen en este Top 10 (como los Legendarios o especies como Beldum) poseen un Catch Rate mínimo de 3\. Matemáticamente, esto significa que, lanzando una Pokéball con el Pokémon a salud máxima, la probabilidad de éxito es de apenas un 1.6%. Esto obliga a trazar estrategias de desgaste, reduciendo salud, y utilizar estados como parálisis o sueño antes de intentar la captura.

## **Gráfica 3: Comparativa de Fortalezas y Debilidades**

Utilizando un mapa de calor, esta gráfica contrasta la resistencia de los mejores Pokémon agrupados por tipo contra los distintos elementos de ataque.

* Los colores más cálidos indican vulnerabilidades críticas (daño x2 o x4), mientras que los colores fríos o neutros indican resistencias o inmunidades (daño x0.5 o x0). Esta herramienta es esencial, ya que permite detectar "cuellos de botella" defensivos. Por ejemplo, el tipo Acero brilla por su alta cantidad de resistencias, convirtiéndose en el tipo defensivo por excelencia.

## 

## **Gráfica 4: Pokémons vs. Regigigas**

Se diseñó una estrategia de combate específica para enfrentar a Regigigas, un Pokémon Legendario de tipo Normal con estadísticas ofensivas masivas. El equipo seleccionado garantiza la máxima probabilidad de victoria mediante la siguiente sinergia:

* **Fortalezas de Tipos:** Regigigas, al ser tipo Normal, tiene una única debilidad: el tipo Lucha. Por ello, el 75% del equipo táctico (Machamp, Lucario y Buzzwole) posee este tipo, garantizando ataques con bonificación de daño súper eficaz (x2).  
* **Habilidades Estratégicas:** El análisis considera la habilidad pasiva de Regigigas, "Inicio Lento", la cual reduce su Ataque y Velocidad a la mitad durante los primeros 5 turnos. El equipo está diseñado para aprovechar esta ventana y asestar daño letal antes de que el Legendario recupere su poder.  
* **Probabilidad de Victoria e Inmunidad:** Se incluyó a Gengar (tipo Fantasma) debido a su inmunidad contra los ataques tipo Normal. Esto permite rotar al equipo de forma segura sin recibir daño de los ataques principales de Regigigas, asegurando hasta un 95% de probabilidad de victoria en la simulación.


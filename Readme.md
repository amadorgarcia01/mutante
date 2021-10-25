API que Valida si una Cadena de ADN suministrada pertenece a un mutante o no.

Para esta validación se ejecutan las siguientes reglas:
- Que las cadenas de ADN solo tengan las letras permitidas
- Que alguna de las letras se repita N veces seguidas en algún segmento de la
  cadena de ADN
- Las letras pueden repetirse dentro de una matriz de segmentos de ADN de forma:
  Horizontal, Vertical o Diagonal
- Los análisis se ejecutan de Izquierda a Derecha, De arriba a abajo
- En BBDD se guardan las Cadenas de ADN analizadas y no se pueden repetir

Los valores de configuración actual son los siguientes:
- Letras permitidas en la cadena de ADN = "ATCG"
- Cantidad de veces seguidas que debe repetirse alguna de las letras
  permitidas = 4
- Cantidad de letras seguidas que componen cada segmento de ADN = 6

Para ejecutar la API se deben consumir los siguientes servicios POST
- Validar el ADN:
  http://35.175.141.199:3000/mutante

  Ejemplos del JSON Cadena de ADN que deben pasarse como parámetro al consumir
  la API:
  - Mutante
    {"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}
  - No Mutante
    {"dna":["ATGCGA","CAGTGC","TTATTT","AGACGG","GCGTCA","TCACTG"]}

- Consultar la relación en ADN Mutante y No Mutante y sus cantidades:
  http://35.175.141.199:3000/stats

  No requiere parámetros, se puede consumir adicionalmente por GET

- BBDD implementada: MySql

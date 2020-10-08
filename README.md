# EvoLagoon

En este proyecto se simula un ecosistema de peces en una laguna de baja profundidad (modelada en 2D). <br>
Hay peces herbívoros, omnívoros y carnívoros. <br>

Los peces carnívoros pueden comer peces más pequeños que ellos, <br>
los herbívoros comen algas que van apareciendo procedimentalmente, <br>
y los omnívoros pueden comer ambas cosas, aunque tienen una penalización energética por esta ventaja.

Cada pez tiene una cantidad de **energía**; moverse resta energía, mientras que comer da energía. <br>
Si un pez logra conseguir suficiente energía puede reproducirse, creando un nuevo pez con una genética muy similar (aunque con pequeñas mutaciones). <br>
Si un pez se queda sin energía muere y desaparece de la laguna. <br>

Según las condiciones del ecosistema (cantidad de algas, gasto energético, etc.) se puede llegar a estados muy distintos, <br>
muchas veces análogos a ecosistemas terrestres. <br>

<img scr = "images/lagoon_img_01.png" width = 600>

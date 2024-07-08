# Cache-simulator-IE0521

## Estructura del directorio

Este repositorio está organizado de la siguiente manera.

```
.
├── results                  directorio de destino de todos los resultados.
├── src
│   ├── base_parte1          código fuente para el caché de un nivel.
│   └── base_parte2          código fuente para el caché multinivel.
├── traces                   directorio con los traces.
├── multi_cache.sh           script en bash para correr simulaciones del caché multinivel.
├── README.md                este archivo.
├── single_cache.sh          script en bash para correr simulaciones del caché de un nivel.
└── test.sh                  script en bash para generar resultados de la guía.
```

## Simulaciones (manual)
Las simulaciones se pueden correr de forma manual. El simulador utiliza los mismos
argumentos que aparecen en el enunciado.

Para correr la simulación haga `cd` a este directorio y escriba en terminal
`python3 ./src/base_parte[1-2]/cache_sim.py <argumentos> -t ./traces/<trace>` 

## Simulaciones (automatizado)

Para facilitar la generación de resultados, se puede utilizar los scripts
proporcionados en este directorio. Las instrucciones se muestran a continuación.

1. Hacer `cd` a este directorio.
2. Para generar los resultados del caché con un nivel, escriba en terminal `./single_cache.sh`.
3. Para generar los resultados del caché multinivel, escriba en terminal `./multi_cache.sh`.
4. Esperar que se generen los resultados en `./results/`.

Nota: estos scripts itera sobre todas las variaciones solicitadas, por lo que su
duración es larga. Si se desea generar resultados de una sola variación o
configuración puede pasarle argumentos a los scripts.

Para el caché de un nivel los argumentos son:
- `s` variar solo el tamaño del caché.
- `a` variar solo la asociatividad.
- `b` variar solo el tamaño del bloque.
- `p` variar solo la política de reemplazo.

Para el caché multinivel los argumentos son:
- `1` solo configuración con un nivel.
- `2` solo configuración con dos niveles.
- `3` solo configuración con tres niveles.

Por ejemplo, si solo se desea variar la asociatividad del caché con un nivel,
escriba en terminal `./single_cache.sh a`. Ahora, si solo se desea generar datos
de todas las configuraciónes del caché con tres niveles, escriba en terminal
`./multi_cache.sh 3`.

Si aparece un error de permisos con los script, ejecute 
`chmod +x single_cache.sh`
`chmod +x multi_cache.sh`
para habilitar permisos de ejecución.

### Formato de los resultados
Los resultados son desplegados en formato csv.

#### Caché de un nivel
Los resultados del caché de un nivel tienen las siguientes columnas (de izquierda a derecha):
- parámetro a variar
- tamaño
- asociatividad
- bloque
- política
- trace
- miss total
- miss rate

#### Caché multinivel
Los resultados del caché de multinivel tienen las siguientes columnas (de izquierda a derecha):
- configuración
- tamaño del último nivel de caché
- asociatividad del último nivel de caché
- trace
- miss total de L1
- miss rate de L1
- miss total de L2 (solo para caché con L2 o L3)
- miss rate de L2 (solo para caché con L2 o L3)
- miss total de L3 (solo para caché con L3)
- miss rate de L3 (solo para caché con L3)
[Read in English](findings.md) · [Volver al README](../README.es.md)

# Los 19 hallazgos

Cada hallazgo sale de la revisión escrita de la especificación (sección "Huecos y dudas", puntos 1 a 19) y de los tres lugares donde la propia especificación dejó una fórmula vacía. No se agregó nada después. Los nombres están anonimizados y el texto de la especificación va parafraseado, nunca copiado.

**Escala de severidad**

| Nivel | Qué significa |
|---|---|
| Bloqueante | No se puede construir ni probar esa parte hasta que alguien responda |
| Alta | Si se construye tal como está, el producto muestra un número malo, hace lo que no es, cuesta más de lo prometido o trae riesgo legal |
| Media | Confunde o no está explicado, pero no frena la construcción |

**Estado:** *Propuesto* quiere decir que la revisión sugirió un cambio concreto. *Abierto* quiere decir que quedó como pregunta para el dueño del producto.

Los hallazgos F01 a F08 los recalcula [`check_numbers.py`](../check_numbers.py).

## A. Números que no cuadran

### F01 · La deduplicación pasa solo por un lado y nadie dice por qué
- **Qué decía:** las fuentes sociales traen unas 1.334 señales y las web unas 1.158; después de deduplicar quedan 2.070 únicas. La tarjeta del KPI las reparte como "1.334 social · 736 web".
- **Por qué es un problema:** 1.334 + 1.158 = 2.492, así que se quitaron 422 señales (17 %). La tarjeta conserva las 1.334 sociales, o sea que todo duplicado fue web: 36 % de lo web eliminado y 0 % de lo social. Puede ser cierto, pero la regla de deduplicación nunca se describe, y así nadie la puede construir ni probar.
- **Cómo se detectó:** sumando los totales de las dos fuentes, comparando con el total de únicas y cruzando con el subtítulo de la tarjeta.
- **Severidad:** Media.
- **Decisión / propuesta:** Propuesto. Deduplicar por el id externo del post o del anuncio, en código, y tratar las cifras de la demo como ejemplos, no como requisitos.

### F02 · 85 % de amenazas y 67 % de ruido no pueden ser ciertos a la vez
- **Qué decía:** "Amenazas marcadas: 1.753" de 2.070 señales, y un filtro de ruido del 67 %.
- **Por qué es un problema:** 1.753 es el 85 % de 2.070. Si el 67 % es ruido, como máximo el 33 % (683 señales) puede ser otra cosa. Los dos números principales se contradicen.
- **Cómo se detectó:** pasando los dos KPI a porcentaje del mismo total.
- **Severidad:** Alta. Son los dos números con los que abre el tablero.
- **Decisión / propuesta:** Abierto. El dueño tiene que definir qué cuenta como amenaza y qué como ruido.

### F03 · El "ruido" es 67 % en un lado y 4 % en otro
- **Qué decía:** ruido filtrado = 67 %; en la taxonomía de etiquetas, `ignore` = 4 %.
- **Por qué es un problema:** se mezclan dos ideas distintas de "ruido" (una clasificación y un tipo de movimiento) y los números no cuadran.
- **Cómo se detectó:** comparando el KPI con la distribución de etiquetas de la sección de reglas de negocio.
- **Severidad:** Media.
- **Decisión / propuesta:** Abierto, junto con F02.

### F04 · Escalados: ¿31, 2 o 2? Y el resumen promete 3 acciones y muestra 2
- **Qué decía:** la tarjeta del KPI dice "31 escalados a una persona"; la barra del flujo dice "2 escalados"; el panel de revisión humana lista 2. La barra también dice "3 acciones" y el resumen muestra 2.
- **Por qué es un problema:** la bandeja humana es la salida principal del sistema. Tres partes de la misma pantalla dan dos conteos distintos.
- **Cómo se detectó:** buscando cada lugar donde aparece la misma cantidad y comparándolos.
- **Severidad:** Alta.
- **Decisión / propuesta:** Abierto.

### F05 · A la lista de competidores le faltan 2 competidores y 553 señales
- **Qué decía:** se vigilan 14 competidores. Lista 12 con su volumen semanal. El componente del grafo dibuja 7.
- **Por qué es un problema:** los 12 volúmenes suman 1.517, no 2.070. 553 señales (27 %) no son de nadie. Tres conteos de competidores: 14, 12 y 7.
- **Cómo se detectó:** sumando la lista por competidor y contando cuántos trae.
- **Severidad:** Media.
- **Decisión / propuesta:** Abierto. El dueño nombra de 3 a 5 competidores reales para la primera versión.

### F06 · Una ventana "semanal" que dura 38 días
- **Qué decía:** "ventana semanal (ej. 20 ago – 27 sep)".
- **Por qué es un problema:** ese rango tiene 38 días. Todo conteo semanal depende de qué es "una semana".
- **Cómo se detectó:** contando los días del ejemplo.
- **Severidad:** Media.
- **Decisión / propuesta:** Abierto.

### F07 · "Tokens procesados" deja por fuera el 99 % de los tokens
- **Qué decía:** "Tokens procesados: 24.849", descritos como 12 tokens de salida por señal; en otra parte dice que la entrada es de unos 1.000 tokens por señal.
- **Por qué es un problema:** la entrada son unos 2,07 millones de tokens, el 99 % del total, y no aparece en el KPI que dice contar tokens.
- **Cómo se detectó:** multiplicando la entrada por señal que da la propia especificación por el número de señales.
- **Severidad:** Media.
- **Decisión / propuesta:** Abierto. El KPI tiene que decir qué tokens cuenta.

## B. Costos y latencias presentados como hechos

### F08 · El gasto semanal cubre solo una parte de la cuenta
- **Qué decía:** gasto semanal $0,2087, "$0,0001 por llamada de 4 juicios".
- **Por qué es un problema:** $0,2087 cuadra con unos 2,07 M de tokens de entrada a $0,10 por millón, o sea que cuenta solo la entrada del clasificador. No incluye el raspado, la búsqueda web ni el modelo que escribe el resumen semanal. El costo real es mayor.
- **Cómo se detectó:** devolviéndose del precio a tokens × precio unitario, y después listando cada componente pago de la arquitectura para ver cuáles cubre el número.
- **Severidad:** Alta. Con ese número se decide el presupuesto.
- **Decisión / propuesta:** Propuesto. Una tabla de costos por componente: unos $0–1 al mes para una primera versión con 5 competidores y unos $6–20 al mes con 14. Precios por verificar antes de pagar.

### F09 · Un requisito de latencia para un proceso que corre una vez por semana
- **Qué decía:** la latencia P50 de 214 ms por señal es un requisito no funcional, y la interfaz muestra la insignia "EN VIVO / tiempo real".
- **Por qué es un problema:** en un lote semanal la latencia no importa. Un modo por lotes que tarda horas sale cerca de 50 % más barato. "Tiempo real" choca con "semanal".
- **Cómo se detectó:** comparando cada requisito no funcional con la forma en que el sistema corre de verdad.
- **Severidad:** Media.
- **Decisión / propuesta:** Propuesto. Clasificar por lotes; quitar el requisito de latencia y el "EN VIVO".

### F10 · Tres pruebas de aceptación que repiten los números de la demo
- **Qué decía:** una prueba exige un gasto semanal de $0,2087 ± $0,01, otra que el medidor de ruido marque 67 % y otra que la P50 esté entre 200 y 250 ms.
- **Por qué es un problema:** una prueba tiene que comprobar comportamiento, no reproducir una semana de datos ajenos. Con datos reales estas pruebas fallan aunque el sistema funcione, o pasan aunque no funcione.
- **Cómo se detectó:** preguntando, para cada prueba, "¿qué comportamiento demuestra?".
- **Severidad:** Alta.
- **Decisión / propuesta:** Propuesto. Una prueba con 10 señales fijas que revise el contrato de salida (JSON estricto) y las reglas de escalado.

## C. Cosas sin definir

### F11 · El clasificador tiene nombre y nada más
- **Qué decía:** cada señal la juzga el "Clasificador X".
- **Por qué es un problema:** no hay proveedor, ni endpoint, ni precio. No se puede construir ni costear.
- **Cómo se detectó:** siguiendo cada caja de la arquitectura hasta un proveedor, una API y un precio.
- **Severidad:** Bloqueante.
- **Decisión / propuesta:** Propuesto. Usar un LLM general pequeño y barato con salida JSON estructurada.

### F12 · Tres de las seis fórmulas de KPI están vacías
- **Qué decía:** las fórmulas de "señales ingeridas", "gasto semanal" y "% de ruido" están vacías (la misma especificación las marca como vacías en el original); `threat_score` no tiene fórmula.
- **Por qué es un problema:** no se puede implementar ni probar un número que nadie definió.
- **Cómo se detectó:** revisando que cada KPI y cada puntaje tenga fórmula.
- **Severidad:** Bloqueante.
- **Decisión / propuesta:** Abierto.

### F13 · El umbral de 0,85 se apoya en probabilidades que nadie calibró
- **Qué decía:** escalar cuando las probabilidades de "mismo comprador" y de "responder esta semana" sean ambas ≥ 0,85; una prueba espera que el modelo "discrimine con precisión".
- **Por qué es un problema:** las probabilidades que escribe un LLM no están calibradas. Sin un conjunto etiquetado, 0,85 es arbitrario y la "precisión" no se puede medir.
- **Cómo se detectó:** preguntando contra qué verdad se medirían el umbral y la prueba.
- **Severidad:** Alta.
- **Decisión / propuesta:** Propuesto. Una fase de calibración: el dueño marca unas 100 señales como útil o ruido; con eso se mide la precisión y se ajustan el prompt y los umbrales.

### F14 · Etiquetas que el modelo no puede saber, y una sola etiqueta donde caben dos
- **Qué decía:** el modelo escoge una etiqueta de una lista que incluye `14_days_live` y `repeat_3_plus_times`.
- **Por qué es un problema:** cuánto lleva un anuncio y cuántas veces se repite algo salen de los datos (fecha de inicio del anuncio, historial), no de leer el texto. Y un anuncio con 18 días es a la vez `paid_ad` y `14_days_live`; una sola etiqueta no alcanza.
- **Cómo se detectó:** preguntando, campo por campo, quién sabe de verdad ese dato; y revisando que las etiquetas se excluyan entre sí.
- **Severidad:** Alta.
- **Decisión / propuesta:** Propuesto. Calcular en código los días activos y las repeticiones; dejar el modelo solo para el juicio.

### F15 · Una sola regla inunda la bandeja humana
- **Qué decía:** todo anuncio con 14 días o más va directo a revisión humana.
- **Por qué es un problema:** el ejemplo de la misma especificación dice que el Competidor 6 tiene 340 anuncios, 42 de ellos con más de 14 días. Ese competidor solo ya mete 42 elementos en la bandeja.
- **Cómo se detectó:** estimando cuántos elementos dispara cada regla con los números de la propia especificación.
- **Severidad:** Alta.
- **Decisión / propuesta:** Abierto. Quedó señalado como riesgo.

### F16 · Una herramienta de búsqueda a la que le piden detectar cambios
- **Qué decía:** escalar cuando la fuente web "detecte" una herramienta gratis nueva o un cambio en el titular o el precio de la página principal (ejemplo: el Competidor 7 lanzó una calculadora gratis).
- **Por qué es un problema:** una API de búsqueda encuentra páginas; no dice qué cambió. Para detectar un cambio hay que guardar copias de cada página y compararlas, y el esquema no tiene tabla para eso.
- **Cómo se detectó:** revisando si cada herramienta puede hacer lo que su regla necesita y buscando esos datos en el esquema.
- **Severidad:** Bloqueante para esa regla.
- **Decisión / propuesta:** Propuesto. Descargar 2–3 URL por dominio y compararlas con la copia anterior (gratis, sin API de búsqueda para esto).

### F17 · La base de datos no aguanta el ciclo de vida del propio sistema
- **Qué decía:** una sola evaluación por señal (`UNIQUE signal_id`), sin campo de semana, sin fecha de inicio del anuncio y con un estado de revisión sin revisor.
- **Por qué es un problema:** no se puede reclasificar una señal, agrupar por semana, calcular cuánto lleva un anuncio ni saber quién revisó algo y con qué nota.
- **Cómo se detectó:** recorriendo el esquema por todo el ciclo: ingerir, clasificar, reclasificar, revisar y reportar por semana.
- **Severidad:** Alta.
- **Decisión / propuesta:** Abierto.

### F18 · Falta lo central: nuestra oferta y nuestro comprador
- **Qué decía:** la pregunta 3 ("¿apunta a nuestro mismo comprador?") lee nuestra oferta y nuestro comprador ideal de una tabla de configuración. La especificación trae la tabla pero no el contenido, y los competidores son figuras públicas de una demo ajena.
- **Por qué es un problema:** sin nuestra oferta, nuestro comprador y nuestros competidores reales, la pregunta 3 no responde nada.
- **Cómo se detectó:** siguiendo las entradas de cada pregunta del modelo hasta el origen de los datos.
- **Severidad:** Bloqueante.
- **Decisión / propuesta:** Abierto. Las dos primeras preguntas para el dueño: la oferta exacta y el comprador ideal en 2–3 líneas, y de 3 a 5 competidores reales con sus cuentas.

### F19 · Raspar las redes sociales grandes incumple sus términos de uso
- **Qué decía:** recoger posts y anuncios de tres redes sociales y de una biblioteca de anuncios con un servicio de raspado.
- **Por qué es un problema:** raspar esas plataformas va contra sus términos de uso. El servicio de raspado se encarga de la parte técnica, no de la legal. La API oficial de la biblioteca de anuncios solo cubre anuncios políticos o sociales, salvo en la UE.
- **Cómo se detectó:** revisando cada fuente de datos contra sus términos y su API oficial.
- **Severidad:** Alta.
- **Decisión / propuesta:** Abierto. Qué canales entran en la primera versión es una de las decisiones del dueño.

## Qué salió de la revisión

La revisión terminó en un plan por fases en vez de una construcción:

| Fase | Qué | Puerta |
|---|---|---|
| P0 · Definir | Cero código. El dueño responde 7 preguntas (oferta y comprador, 3–5 competidores reales, canales, clasificador, a dónde llega el resumen, dónde corre, la interfaz después) | Respuestas en la mano |
| P1 · MVP (1–2 días) | Un script, sin interfaz, programado cada semana. Deduplicación por id externo; días activos y cambios web calculados en código; clasificación por lotes con JSON estricto; un resumen corto que llega por mensaje | Una prueba con 10 señales fijas: contrato JSON y reglas de escalado |
| P2 · Calibrar (2–4 semanas de uso) | El dueño marca unas 100 señales; se mide la precisión y se ajustan prompt y umbrales; repeticiones a partir del historial | Precisión medida, no supuesta |
| P3 · Interfaz | Un tablero de solo lectura; para empezar basta una tabla de amenazas | Solo si P2 demuestra valor |
| P4 · Escalar | 14 o más competidores | |

La lectura general: la especificación parecía armada a partir de la captura de la demo de otra empresa (una cabecera con el nombre de esa empresa, competidores que son figuras públicas reales y los números de una sola semana escritos como requisitos). Esa observación explica buena parte de los hallazgos.

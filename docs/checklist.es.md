[Read in English](checklist.md) · [Volver al README](../README.es.md)

# Checklist para revisar especificaciones

Cópiala en el ticket o en el documento de revisión y márcala antes de que alguien escriba código. Cada línea existe porque un hallazgo real de este caso la necesitó (entre corchetes).

## 0. Leer una vez para entender la intención
- [ ] Puedo decir en 5 líneas qué hace el sistema, y el dueño está de acuerdo.
- [ ] Sé de dónde salió la especificación. Si se armó con una captura o con la demo de otro, sus números son ejemplos, no requisitos. [F01–F10]

## 1. Recalcular cada número
- [ ] Las partes suman los totales (fuentes → únicas, lista por elemento → total general). [F01, F05]
- [ ] Los porcentajes del mismo total son compatibles entre sí (si se excluyen, no pueden pasar del 100 %). [F02]
- [ ] Los conteos cuadran con sus listas (14 anunciados = 14 listados = 14 dibujados). [F05]
- [ ] Las ventanas de tiempo cuadran con su nombre ("semanal" = 7 días). [F06]
- [ ] Las unidades están completas: tokens de entrada **y** de salida, cada componente pago en el costo. [F07, F08]

## 2. Cruzar el mismo dato en todas partes
- [ ] La misma cantidad tiene el mismo valor en cada sección, tarjeta, barra y panel. [F04]
- [ ] La misma palabra significa lo mismo en todo el documento ("ruido" como clase y como etiqueta). [F03]
- [ ] Lo que promete un prompt o una regla (por ejemplo "máximo 3 acciones") cuadra con lo que muestra el diseño. [F04]

## 3. Seguir cada requisito hasta su origen
- [ ] Cada KPI y cada puntaje tiene una fórmula escrita. [F12]
- [ ] Cada caja de la arquitectura tiene proveedor, API y precio. [F11]
- [ ] Cada campo dice quién lo sabe: el modelo, los datos o una persona. Lo que sale de los datos se calcula en código. [F14]
- [ ] Las etiquetas de una lista de opción única se excluyen entre sí. [F14]
- [ ] Cada herramienta puede hacer de verdad lo que su regla le pide (buscar ≠ detectar cambios). [F16]
- [ ] Las entradas clave existen, con contenido, no solo una tabla para ellas. [F18]
- [ ] El esquema aguanta el ciclo de vida: volver a correr, reclasificar, agrupar por periodo, saber quién revisó qué. [F17]

## 4. Comparar los requisitos con la realidad
- [ ] Los requisitos no funcionales cuadran con la forma en que corre el sistema (nada de meta de latencia para un lote semanal ni de insignia "en vivo" para un proceso semanal). [F09]
- [ ] Cada regla tiene un estimado de volumen, para que ninguna inunde una cola humana. [F15]
- [ ] Los umbrales sobre probabilidades del modelo vienen con un plan de calibración y un conjunto etiquetado. [F13]
- [ ] Las fuentes de datos están permitidas por sus términos de uso y la API oficial cubre lo que se necesita. [F19]

## 5. Revisar las pruebas que trae la especificación
- [ ] Cada prueba de aceptación demuestra un comportamiento; ninguna se limita a repetir los números de la demo. [F10]
- [ ] Todo criterio de "precisión" dice contra qué se mide. [F13]

## 6. Cerrar la revisión
- [ ] Cada hallazgo tiene: qué decía, por qué es un problema, cómo se encontró, severidad y decisión o pregunta.
- [ ] Los bloqueantes se vuelven preguntas para el dueño, numeradas y que se respondan en minutos.
- [ ] La construcción se parte en fases, cada una con su puerta; la interfaz llega cuando el valor ya está demostrado.

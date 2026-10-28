# IS1
repositorio para el proyecto integrador de ingeniería de software1

Luciano  Matias Mattiauda   github: (pichonTT)  dni: 41378912

Ivo Mirko Elián  Narváez    github: IvoMirkoE22 dni: 42786377

Damian Flauta Gamarra       github: damizpy     dni: 44614239


Explicacion: 
PATRÓN STRATEGY USADO

1. Estrategia

GenerarRespuestaStrategy

Es la interfaz que define la operación común:

generarRespuesta(Pregunta p) : String

Permite que distintos proveedores de IA generen respuestas a través de una misma interfaz.


2. Estrategias Concretas

EstrategiaOpenAI

EstrategiaGemini

EstrategiaModeloLocal

Implementan la interfaz GenerarRespuestaStrategy.

Cada estrategia resuelve la generación de respuestas utilizando su proveedor específico.


3. Contexto

AgenteIA

Utiliza una referencia a GenerarRespuestaStrategy y no depende directamente de una estrategia concreta.

De esta forma puede reemplazarse un proveedor por otro sin modificar el diseño central del agente.

Por ejemplo:

- OpenAI
- Gemini
- Modelo Local

son intercambiables para el AgenteIA.


Diferencia entre Autor y Strategy

Autor

Representa quién produce o firma una respuesta.

Puede ser:

- Usuario
- AgenteIA


Strategy

Representa cómo se genera el contenido automático.

Puede ser:

- EstrategiaOpenAI
- EstrategiaGemini
- EstrategiaModeloLocal


Relación entre ambos

No son la misma cosa.

Un AgenteIA puede ser el autor de una respuesta y, al mismo tiempo, utilizar cualquiera de las estrategias disponibles para generar el contenido.

Por ejemplo:

AgenteIA (autor)
        |
        +----> EstrategiaOpenAI

AgenteIA (autor)
        |
        +----> EstrategiaGemini

AgenteIA (autor)
        |
        +----> EstrategiaModeloLocal

Es decir:

- Autor responde a la pregunta: ¿Quién escribió la respuesta?
- Strategy responde a la pregunta: ¿Cómo se generó la respuesta?

Esa distinción suele ser la clave para entender por qué en el TP aparecen tanto la abstracción de Autor como el patrón Strategy.

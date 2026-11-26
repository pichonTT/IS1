# IS1 — Comunidad de preguntas y respuestas

Proyecto Integrador de **Ingeniería de Software I**.

IS1 es una aplicación web que permite a los usuarios compartir preguntas, publicar respuestas, votar contenidos y recibir asistencia automática mediante un agente de inteligencia artificial.

## Funcionalidades

- **Usuarios:** registro e inicio de sesión.
- **Preguntas:** publicación, listado, consulta y búsqueda.
- **Categorías y etiquetas:** clasificación de las preguntas.
- **Respuestas:** publicación de respuestas por parte de los usuarios.
- **Respuestas aceptadas:** el autor de una pregunta puede seleccionar una respuesta como aceptada.
- **Votaciones:** votos positivos y negativos sobre preguntas y respuestas. Cada usuario puede modificar su voto.
- **Asistencia de IA:** generación de respuestas mediante la etiqueta `ia-help` o a través de una solicitud manual.
- **Automatización:** revisión periódica de preguntas sin respuesta mediante un programador de tareas.
- **API REST:** operaciones disponibles mediante endpoints HTTP.
- **Interfaz web:** acceso a las funcionalidades principales desde el navegador.

> **Nota sobre IA:** las estrategias Gemini, OpenAI y local están simuladas en esta versión del proyecto. No se realizan consultas reales a esos proveedores.

## Tecnologías utilizadas

- Python 3.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate y Alembic
- SQLite
- SQLAlchemy
- APScheduler
- Pytest
- Ruff
- HTML, CSS y Jinja2
- uv para la gestión del proyecto y sus dependencias

## Requisitos

- Python 3.13 o superior.
- uv instalado.
- Git para obtener el repositorio.

## Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd IS1
```

Instalar las dependencias:

```bash
uv sync
```

Configurar las variables de entorno en Git Bash:

```bash
export SECRET_KEY="una-clave-segura-para-desarrollo"
export DATABASE_URL="sqlite:///is1.db"
```

El archivo `.env.example` contiene una plantilla de configuración. La aplicación obtiene estas variables desde el entorno del sistema.

## Base de datos

Para crear o actualizar la estructura de la base de datos, ejecutar:

```bash
uv run flask --app 'is1:create_app' db upgrade
```

Las migraciones se encuentran en la carpeta `migrations/`.

<< Configuración inicial de la base de datos >>

Después de clonar el repositorio, instalar las dependencias y ejecutar las migraciones, es necesario cargar las categorías iniciales.

1. Instalar dependencias

  uv sync

2. Crear o actualizar la estructura de la base de datos

  uv run flask --app 'is1:create_app' db upgrade

3. Cargar las categorías iniciales

Ejecutar desde la carpeta raíz del proyecto:

uv run python - <<'PY'
import sqlite3

conexion = sqlite3.connect("src/instance/is1.db")

for nombre in ("Programacion", "Programación"):
    existe = conexion.execute(
        "SELECT 1 FROM categoria WHERE nombre = ?",
        (nombre,)
    ).fetchone()

    if not existe:
        conexion.execute(
            "INSERT INTO categoria (nombre) VALUES (?)",
            (nombre,)
        )

conexion.commit()

print("Categorías cargadas correctamente:")
print(conexion.execute(
    "SELECT id, nombre FROM categoria"
).fetchall())

conexion.close()
PY

Este procedimiento evita insertar categorías duplicadas cuando se ejecuta nuevamente.

4. Ejecutar la aplicación

    uv run flask --app 'is1:create_app' run

    Abrir en el navegador: http://127.0.0.1:5000

5. Crear un usuario

  Registrarse desde la interfaz web para comenzar a utilizar la aplicación, publicar preguntas, responder y votar.

## Ejecución

Iniciar el servidor de desarrollo:

```bash
uv run flask --app 'is1:create_app' run
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## API REST

Los principales endpoints disponibles son:

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Verificar el estado del servidor |
| POST | `/usuarios` | Registrar un usuario |
| GET | `/preguntas` | Listar preguntas |
| POST | `/preguntas` | Crear una pregunta |
| GET | `/preguntas/<id>` | Consultar una pregunta |
| POST | `/preguntas/<id>/respuestas` | Crear una respuesta |
| POST | `/preguntas/<id>/respuestas/ia` | Generar respuesta de IA |
| PATCH | `/preguntas/<id>/respuestas/<respuesta_id>/aceptar` | Aceptar una respuesta |
| POST | `/preguntas/<id>/votos` | Votar una pregunta |
| POST | `/respuestas/<id>/votos` | Votar una respuesta |
| POST | `/automatizacion/ia/preguntas-sin-respuesta` | Ejecutar revisión automática manualmente |

La interfaz web también dispone de rutas propias para registro, inicio de sesión, publicación y consulta de preguntas, respuestas y votos.

## Pruebas y calidad

Ejecutar las pruebas automatizadas:

```bash
uv run pytest -v
```

Verificar el estilo y la calidad del código:

```bash
uv run ruff check .
```

Verificar el archivo de dependencias:

```bash
uv lock --check
```

## Estructura del proyecto

```text
IS1/
├── migrations/             # Migraciones de la base de datos
├── src/
│   └── is1/
│       ├── api/            # Endpoints de la API REST
│       ├── models/         # Modelos de datos
│       ├── services/       # Servicios y automatización de IA
│       ├── static/         # Archivos CSS
│       ├── templates/      # Plantillas HTML
│       ├── web/            # Rutas de la interfaz web
│       ├── config.py       # Configuración
│       └── __init__.py     # Creación de la aplicación
├── tests/                  # Pruebas automatizadas
├── .env.example            # Plantilla de configuración
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Integrantes

- **Luciano Matias Mattiauda** — [GitHub: pichonTT](https://github.com/pichonTT)
- **Ivo Mirko Elian Narvaez** — [GitHub: IvoMirkoE22](https://github.com/IvoMirkoE22)
- **Damian Flavio Gamarra** — [GitHub: damizpy](https://github.com/damizpy)

---

**Proyecto Integrador — Ingeniería de Software I**

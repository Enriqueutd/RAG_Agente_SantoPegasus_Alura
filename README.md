# 🦄 Santo Pegasus Soluciones - Asistente Virtual RAG

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange)

---

# 📖 Descripción

Este proyecto implementa un **Asistente Virtual Inteligente** basado en la arquitectura **Retrieval-Augmented Generation (RAG)**, desarrollado como parte del **Challenge de Alura Latam + Oracle ONE**.

El asistente fue diseñado para la empresa ficticia **Santo Pegasus Soluciones**, permitiendo realizar consultas en lenguaje natural sobre documentación técnica interna sin necesidad de revisar manualmente múltiples archivos PDF.

La aplicación utiliza **LangChain** para orquestar el flujo RAG, **ChromaDB** como base de datos vectorial, **HuggingFace Embeddings** para representar semánticamente la información y **Llama 3.3 70B**, ejecutado mediante la API de **Groq**, para generar respuestas fundamentadas únicamente en el contenido de la documentación.

---

# 🎯 Objetivos del proyecto

- Implementar una arquitectura **RAG** utilizando LangChain.
- Consultar documentación técnica mediante lenguaje natural.
- Reducir las alucinaciones del modelo utilizando recuperación semántica.
- Construir una interfaz web sencilla utilizando Streamlit.
- Aplicar buenas prácticas de seguridad mediante variables de entorno.

---

# 🏗 Arquitectura de la solución

El flujo de funcionamiento del sistema es el siguiente:

```text
                  Usuario
                     │
                     ▼
             Streamlit (Interfaz)
                     │
                     ▼
                LangChain
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
 Retriever (ChromaDB)          Llama 3.3
      ▲                             │
      │                             ▼
 Embeddings (MiniLM)          Respuesta final
      ▲
      │
 Documentos PDF
```

---

# ⚙ Funcionamiento

## 1. Carga de documentos

Los archivos PDF se cargan automáticamente desde:

```
documentos_pegasus/
```

mediante:

- PyPDFDirectoryLoader

---

## 2. Procesamiento del texto

Los documentos se dividen en fragmentos utilizando:

- RecursiveCharacterTextSplitter

Configuración utilizada:

- **Chunk Size:** 800
- **Chunk Overlap:** 100

---

## 3. Generación de embeddings

Cada fragmento es convertido en un vector utilizando el modelo:

```
sentence-transformers/all-MiniLM-L6-v2
```

Posteriormente se almacena en **ChromaDB**.

---

## 4. Recuperación y generación

Cuando el usuario realiza una pregunta:

1. Se calcula el embedding de la consulta.
2. Se recuperan los fragmentos más similares.
3. LangChain construye el contexto.
4. Llama 3.3 genera una respuesta basada únicamente en la documentación.

---

# 🛠 Tecnologías utilizadas

| Tecnología | Función |
|------------|---------|
| Python 3.10+ | Lenguaje principal |
| LangChain | Orquestación del flujo RAG |
| Groq API | Servicio de inferencia |
| Llama 3.3 70B | Modelo de lenguaje |
| HuggingFace Embeddings | Generación de embeddings |
| ChromaDB | Base de datos vectorial |
| Streamlit | Interfaz web |
| python-dotenv | Variables de entorno |

---

# 📂 Estructura del proyecto

```text
RAG_Agente_SantoPegasus_Alura/

│
├── documentos_pegasus/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

---

# 🔐 Variables de entorno

Para proteger la API Key utilizada por Groq, el proyecto emplea un archivo `.env`.

Crea un archivo llamado:

```
.env
```

y agrega la siguiente variable:

```env
GROQ_API_KEY=tu_api_key
```

> **Importante:** El archivo `.env` se encuentra excluido mediante `.gitignore` para evitar la exposición de credenciales.

---

# ⚙ Instalación

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Enriqueutd/RAG_Agente_SantoPegasus_Alura.git

cd RAG_Agente_SantoPegasus_Alura
```

---

## 2️⃣ Crear un entorno virtual

### Windows

```powershell
python -m venv .venv

.\.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configurar la API

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
GROQ_API_KEY=tu_api_key
```

---

## 5️⃣ Agregar la documentación

Coloca todos los archivos PDF dentro de:

```
documentos_pegasus/
```

---

## 6️⃣ Ejecutar la aplicación

```bash
streamlit run app.py
```

---

# 💬 Ejemplos de consultas

- ¿Cuáles son los canales oficiales de comunicación interna?
- ¿Quién puede declarar formalmente un incidente?
- ¿Cuáles son las responsabilidades del equipo SRE?
- ¿Qué protocolo se sigue para realizar un post-mortem?
- ¿Qué tecnologías utiliza la arquitectura de microservicios?

---

# 📷 Capturas de pantalla

## Pantalla principal

*(Agregar captura de la interfaz.)*

---

## Ejemplo de consulta

*(Agregar captura de una consulta realizada.)*

---

## Respuesta generada

*(Agregar captura de la respuesta obtenida.)*

---

# ☁ Despliegue

La aplicación se encuentra preparada para ser desplegada en **Streamlit Community Cloud**.

Para ello únicamente es necesario:

- Conectar el repositorio de GitHub.
- Configurar la variable `GROQ_API_KEY` en la sección **Secrets**.
- Seleccionar `app.py` como archivo principal.

---

# 🚀 Posibles mejoras

- Soporte para archivos Word (.docx).
- Memoria conversacional.
- Historial persistente de consultas.
- Carga dinámica de documentos desde la interfaz.
- Citación automática de las páginas consultadas.
- Autenticación de usuarios.



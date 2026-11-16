# RAG local sobre seguridad en IA generativa

**Autor: Juan Cifuentes**

**Fecha: noviembre de 2026**

**Trabajo Integrador de Técnicas de Procesamiento de Habla, IFTS N.º 24, segundo cuatrimestre de 2026.**

---

## 1. Problema y destinatario

Este sistema permite que un analista de seguridad consulte riesgos de la IA generativa y cómo mitigarlos en tres guías de referencia en español (OWASP, AESIA e INCIBE).

Responde preguntas cuya respuesta está escrita en esas guías, por ejemplo qué es la inyección de prompt o qué exige el artículo 15 del Reglamento Europeo de IA. No sirve para estadísticas, incidentes reales, comparaciones entre productos ni normativa de otros países.

---

## 2. Corpus

Los PDF están en `datos/` y son copias de los originales, descargadas el 10/11/2026.

| Archivo                                                                     | Autoría                     | Origen                                                                                                         | Fecha      | Licencia        |
| --------------------------------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------- | --------------- |
| `owasp_top10_llm_2025.pdf` (OWASP Top 10 para Aplicaciones de LLM 2025)   | OWASP GenAI Security Project | https://genai.owasp.org                                                                                        | 11/03/2025 | CC BY-SA 4.0    |
| `aesia_guia11_ciberseguridad.pdf` (Guía 11: Ciberseguridad)              | AESIA                        | https://aesia.digital.gob.es/storage/media/11-guia-ciberseguridad.pdf                                          | 17/07/2026 | CC BY 4.0       |
| `incibe_medidas_ia_frontera.pdf` (Medidas ante modelos de IA de frontera) | INCIBE                       | https://www.incibe.es/sites/default/files/2026-06/Medidas_ciberseguridad_ciberresiliencia_modelos_frontera.pdf | 17/06/2026 | CC BY-NC-SA 4.0 |

Las tres licencias permiten redistribuir citando la fuente. El trabajo no tiene fines comerciales, como pide la de INCIBE.

---

## 3. Arquitectura

| Orden | Componente                         | Librería y versión                    | Valor usado                                                                         |
| ----- | ---------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------- |
| 1     | `PyPDFLoader`                    | langchain-community 0.4.2 (pypdf 7.0.1) | 3 PDF de `datos/`                                                                 |
| 2     | `RecursiveCharacterTextSplitter` | langchain-text-splitters 1.1.3          | `chunk_size=800`, `chunk_overlap=120`                                           |
| 3     | `OllamaEmbeddings`               | langchain-ollama 1.1.0                  | bge-m3                                                                              |
| 4     | `Chroma`                         | langchain-chroma 1.1.0 (chromadb 1.5.9) | Colección `seguridad_ia_bge_m3`, carpeta `chroma_db_bge_m3/`                   |
| 5     | `similarity_search_with_score`   | langchain-chroma 1.1.0                  | `k=3`                                                                             |
| 6     | `ChatPromptTemplate`             | langchain-core 1.7.7                    | Prompt del cuaderno 04 del profesor (unidad 014), en mi cuaderno 03 y en `app.py` |
| 7     | `ChatOllama`                     | langchain-ollama 1.1.0                  | granite4:latest, `temperature=0`                                                  |
| 8     | Gradio                             | gradio 6.31.0                           | `python app.py`                                                                   |

Python 3.12 y Ollama 0.40.16.

Los gráficos de los cuadernos usan `utils_visualizacion.py`, el archivo de la unidad 014 que sólo dibuja resultados que los cuadernos ya calcularon.

---

## 4. Instalación local

Hace falta tener instalado [Ollama](https://ollama.com). El entorno se arma con [uv](https://docs.astral.sh/uv/) y Python 3.12, desde la carpeta del proyecto:

```powershell
uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt
ollama pull granite4:latest
ollama pull bge-m3
```

En Linux y macOS el entorno se activa con `source .venv/bin/activate`. Los pasos del sistema están en los cuadernos `01` a `04`. Para ejecutarlos en VS Code hay que elegir `.venv` con `Ctrl+Shift+P` → *Python: Select Interpreter*.

Con Ollama abierto, la interfaz se abre con:

```powershell
python app.py
```

Queda en `http://127.0.0.1:7860`. Se cierra con Ctrl+C.

---

## 5. Reindexación

La primera vez que se ejecuta `app.py` se crea la carpeta `chroma_db_bge_m3/` con los fragmentos. Tarda unos minutos y después se reutiliza. Si cambian los PDF, el corte o el modelo de embeddings, hay que borrar esa carpeta y volver a ejecutar `python app.py`.

El índice no se publica en GitHub porque está en `.gitignore`, igual que `.venv/` y `.env`.

---

## 6. Pruebas

Las cinco preguntas están en `04_probar_el_rag.ipynb`. Anoté la fuente esperada antes de ejecutar y comparé cada respuesta con el PDF.

| Pregunta                                                                                                   | Fuente esperada         | Fragmento recuperado [1]      | Respuesta                                                                    | Observación                                                                                          |
| ---------------------------------------------------------------------------------------------------------- | ----------------------- | ----------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| ¿Qué es la inyección de prompt?                                                                         | OWASP, p. 8             | OWASP, p. 8 (0,598)           | Da la definición y cita [1].                                                | Correcta. El fragmento [3] es el índice de OWASP.                                                    |
| ¿Qué exige el artículo 15 del Reglamento de IA sobre ciberseguridad?                                    | AESIA, páginas 16 y 18 | AESIA, p. 16 (0,627)          | Un nivel adecuado de ciberseguridad durante todo el ciclo de vida. Cita [1]. | Correcta pero incompleta, le falta «precisión y solidez». El fragmento [3] es el índice de AESIA. |
| ¿Qué medidas se recomiendan para la gestión de identidades y accesos frente a ataques asistidos por IA? | INCIBE, p. 5            | INCIBE, p. 5 (0,660)          | MFA obligatorio y métodos resistentes al phishing. Cita [1].                | Correcta. Nombra sólo la primera medida de la lista.                                                 |
| ¿Cuántos ataques de inyección de prompt hubo en Argentina en 2025?                                      | Ninguna                 | OWASP, p. 3 (índice) (0,820) | «No encuentro esa información en los documentos.»                         | Se abstuvo aunque recibió tres fragmentos.                                                           |
| ¿Cuál es el modelo de IA más seguro del mercado?                                                        | Ninguna                 | INCIBE, p. 4 (0,907)          | «No encuentro esa información en los documentos.»                         | Se abstuvo.                                                                                           |

**Limitaciones observadas**

1. Los índices de los PDF se recuperan como si fueran contenido. Pasó con OWASP y AESIA, y ocupan lugar en el contexto sin aportar nada. En la app, la misma pregunta del artículo 15 escrita con comillas y un punto trajo el índice de AESIA en primer lugar, y el modelo lo citó como [1]. Lo cambiaría quitando esas páginas antes de indexar.
2. La abstención depende del prompt. Chroma siempre devuelve fragmentos, aunque la pregunta no tenga respuesta en el corpus. En las pruebas el modelo se abstuvo, pero no está garantizado.

---

## 7. Decisiones y límites

| Tema           | Decisión                  | Motivo o límite                                                                                                                                              |
| -------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fragmentación | 800 / 120 (480 fragmentos) | Probé 250, 500, 800 y 1100 (1515, 735, 480 y 364 fragmentos). Con 800 la definición de inyección de prompt y el artículo 15 quedan enteros (cuaderno 01). |
| `k`          | 3                          | Valor del material de clase. Con 1 la respuesta no cambió.                                                                                                   |
| Embeddings     | bge-m3                     | Multilingüe. El mismo para indexar y para buscar.                                                                                                            |

---

## 8. Uso de IA

Usé Claude (Anthropic) desde claude.ai. Al principio lo usé sobre todo para resolver los problemas que tuve al instalar y correr el proyecto en Windows 10. Después lo usé para buscar guías en español y revisar sus licencias, y para adaptar app.py.

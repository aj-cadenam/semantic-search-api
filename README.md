# semantic-search-api

# 📌 Proyecto: API Flask para Procesamiento de Embeddings con PostgreSQL y OpenAI

# Descripción General

Este proyecto es una API REST basada en Flask que permite almacenar y recuperar cadenas de texto de manera eficiente utilizando embeddings semánticos generados con OpenAI y almacenados en PostgreSQL con la extensión pgvector.

La API implementa búsquedas por similitud mediante el operador <=>, que calcula la distancia coseno entre los embeddings almacenados y el embedding de consulta. Para mejorar la eficiencia y escalabilidad, se utiliza un enfoque de búsqueda aproximada:

El sistema sigue una **arquitectura hexagonal**, asegurando modularidad y mantenibilidad. Utiliza **Poetry** para la gestión de dependencias y **Docker Compose** para ejecutar los servicios en contenedores, integrando OpenAI, Flask y PostgreSQL de manera eficiente.

---

#Estructura del Proyecto

```
/Semantic-Search
│── /templates               # Plantillas HTML para el frontend
│── /domain                  # Lógica de negocio (Procesamiento de embeddings)
│── /adapters                # Capa de infraestructura (Conexión con DB, API OpenAI)
│── /config                  # Gestión de configuración
│── app.py                   # Aplicación Flask y manejo de rutas
│── pyproject.toml
│── Dockerfile
│── docker-compose.yml
│── README.md
```

---

## Configuración e Instalación

### 1️⃣ **Clonar el Repositorio**

```bash
git clone <repository-url>
```

### 2️⃣ **Configurar Variables de Entorno**

Crear un archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=<tu_clave_api_openai>

DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432
```

### 3️⃣ **Instalar Dependencias con Poetry**

Asegúrate de tener **Poetry** instalado y ejecuta:

```bash
poetry install
```

### 4️⃣ **Ejecutar con Docker Compose**

Para iniciar PostgreSQL, la API Flask y las dependencias:

```bash
docker-compose up --build
```

Esto realizará:

- La configuración de **PostgreSQL** con **pgvector** habilitado.
- El inicio de la **API Flask**.
- La exposición del servicio en `http://localhost:5000/`.

---

## Cómo Funciona

### **Flujo de Procesamiento de Embeddings**

1. **El usuario envía un texto de entrada** a través de un endpoint de la API.
2. **Las rutas de Flask procesan la solicitud** (`app.py`).
3. **Se generan los embeddings** utilizando `text-embedding-ada-002` de OpenAI.
4. **Los embeddings se almacenan** en PostgreSQL con `pgvector`.
5. **Las búsquedas de similitud** se realizan utilizando el operador de distancia coseno (`<=>`).

📌 Explicación del cálculo de similitud con pgvector

embedding <=> %s::vector calcula la distancia de similitud entre el embedding en la base de datos y el proporcionado.

1 - (embedding <=> %s::vector) convierte la distancia en una medida de similitud, donde 1 es idéntico y 0 es completamente diferente.

WHERE 1 - (embedding <=> %s::vector) >= 0.5 filtra solo aquellos embeddings con una similitud de al menos 50%.

ORDER BY embedding <=> %s::vector ordena los resultados del más similar al menos similar.

### **Endpoints**

🔹 Generar y Almacenar Embeddings

POST /get_embedding

Descripción: Este endpoint recibe un texto de entrada, genera su representación numérica (embedding) utilizando el modelo text-embedding-ada-002 de OpenAI y lo almacena en PostgreSQL con la extensión pgvector.

🔹 Buscar Textos Similares

POST /get_similar

Descripción: Este endpoint recibe un texto de entrada, genera su embedding y lo compara con los almacenados en la base de datos. Utiliza la distancia coseno (<=>) para encontrar los textos más similares y devolverlos ordenados por relevancia.

---

## **Tecnologías Utilizadas**

✅ **Flask** – Framework web para manejar la API.  
✅ **PostgreSQL + pgvector** – Almacenamiento y búsqueda de embeddings.  
✅ **OpenAI API (text-embedding-ada-002)** – Modelo de generación de embeddings.  
✅ **Poetry** – Gestión de dependencias.  
✅ **Docker + Docker Compose** – Contenerización del proyecto.  
✅ **Distancia Coseno (`<=>`)** – Métrica de similitud para búsqueda de embeddings.

---

**¡Puedes comenzar a utilizar la API enviando solicitudes a `http://localhost:5000`!**

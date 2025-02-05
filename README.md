# semantic-search-api

# 📌 Proyecto: API Flask para Procesamiento de Embeddings con PostgreSQL y OpenAI

# Descripción General

Este proyecto es una API basada en Flask que procesa cadenas de texto de entrada, las convierte en **embeddings** utilizando el modelo `text-embedding-ada-002` de OpenAI, las almacena en **PostgreSQL** con **pgvector**, y realiza búsquedas de similitud utilizando **distancia coseno (`<=>`)**.

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

````bash
git clone <repository-url>

### 2️⃣ **Configurar Variables de Entorno**
Crear un archivo `.env` en la raíz del proyecto:
```env
OPENAI_API_KEY=<tu_clave_api_openai>
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432
````

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

### **Endpoints**

#### ** Generar y Almacenar Embeddings**

```http
POST /get_embedding
```

#### ** Buscar Textos Similares**

```http
POST /get_similar
```

---

## **Tecnologías Utilizadas**

✅ **Flask** – Framework web para manejar la API.  
✅ **PostgreSQL + pgvector** – Almacenamiento y búsqueda de embeddings.  
✅ **OpenAI API (text-embedding-ada-002)** – Modelo de generación de embeddings.  
✅ **Poetry** – Gestión de dependencias.  
✅ **Docker + Docker Compose** – Contenerización del proyecto.  
✅ **Distancia Coseno (`<=>`)** – Métrica de similitud para búsqueda de embeddings.

---

🚀 **¡Ahora puedes comenzar a utilizar la API enviando solicitudes a `http://localhost:5000`!**

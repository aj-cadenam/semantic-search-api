# Usa una imagen base de Python optimizada
FROM python:3.11

# Instala Poetry a nivel global
RUN pip install poetry

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de Poetry antes del código para aprovechar caché
COPY pyproject.toml poetry.lock ./

# Instala dependencias con Poetry sin entorno virtual, Usa poetry install --no-root --no-dev para evitar instalar dependencias innecesarias dentro del contenedor.Copia pyproject.toml y poetry.lock antes que el código para optimizar la caché de Docker.
RUN curl -sSL https://install.python-poetry.org | python3 -



# Copia el código de la aplicación
COPY . .

# Expone el puerto de Flask
EXPOSE 5000

# Comando para correr la app con Poetry
CMD ["poetry", "run", "python", "app/app.py"]

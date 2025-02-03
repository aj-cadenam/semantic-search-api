# Usa una imagen base de Python optimizada
FROM python:3.12-slim

# Instala Poetry a nivel global
RUN pip install poetry

# Establece el directorio de trabajo
#WORKDIR /app

# Copia los archivos de Poetry antes del código para aprovechar caché
COPY pyproject.toml poetry.lock ./

# Instala las dependencias usando Poetry sin entorno virtual y sin dependencias de desarrollo
#RUN poetry install --no-root
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install


# Copia el código de la aplicación
COPY . .

# Expone el puerto de Flask
EXPOSE 5000

# Comando para correr la app con Poetry
CMD ["poetry", "run", "python", "app.py"]


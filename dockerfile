# Usa una imagen base de Python optimizada
FROM python:3.12-slim

RUN pip install poetry

# Establece el directorio de trabajo
#WORKDIR /app

# Copia los archivos de Poetry antes del código para aprovechar caché
COPY pyproject.toml poetry.lock ./

# Instala las dependencias de la aplicación con Poetry y luego copia el código de la aplicación en el contenedor de Docker.
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install
#RUN poetry install --no-root

COPY . .

# Expone el puerto de Flask
EXPOSE 5000
#Como se ejecuta la aplicacion 
CMD ["poetry", "run", "python", "app.py"]


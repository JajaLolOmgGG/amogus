FROM debian:latest
USER root

ENV DEBIAN_FRONTEND=noninteractive

# Copia los archivos de la aplicación al directorio /app
COPY . /app

# Establece los permisos adecuados para todos los archivos en /app
RUN chmod -R 777 /app

# Establece /app como el directorio de trabajo
WORKDIR /app

# Actualiza los repositorios e instala dependencias necesarias
RUN apt-get update -y && apt-get install -y
	git \
    python3 \
    python3-pip \
    python3-venv \
    p7zip-full \
    wget \
    lib32gcc-s1 \
    lib32stdc++6

# Crea el entorno virtual para Python
RUN python3 -m venv /app/venv

# Actualiza pip e instala las dependencias de Python
RUN /app/venv/bin/pip install -U pip
RUN /app/venv/bin/pip install watchdog uvicorn fastapi

# Extrae el contenido de sv.tar
RUN 7z x sv.tar -y

# Establece permisos para los archivos necesarios
RUN chmod -R 777 /app

CMD ["/app/venv/bin/python", "/app/sv.py"]
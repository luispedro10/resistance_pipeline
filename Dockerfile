# Imagen base
FROM ubuntu:20.04

# Evitar preguntas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar e instalar dependencias del sistema
RUN apt-get update && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion \
    libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 \
    libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

# Instalar Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda.sh \
    && bash /miniconda.sh -b -p /miniconda
ENV PATH="/miniconda/bin:$PATH"

# Crear entornos de Conda
RUN conda create -n tesisenv python=3.8 -y
RUN conda create -n rgi_env python=3.8.5 rgi=6.0.3 pandas=2.0.3 -c bioconda -c conda-forge -y

# Activar el entorno y instalar paquetes
RUN echo "source activate tesisenv" > ~/.bashrc
ENV PATH /opt/conda/envs/tesisenv/bin:$PATH
RUN conda install -n tesisenv fastp=0.22.0 kraken2=2.1.3 openpyxl=3.1.2 prokka=1.14.6 spades=3.15.5 tk=8.6.13 pandas=1.1.5 pyqt -c bioconda -c conda-forge -y

# Copiar el código fuente
COPY . /app
WORKDIR /app

# Configurar volúmenes
VOLUME ["/data", "/dbs"]

# Configuración para GUI
ENV DISPLAY host.docker.internal:0

# Entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

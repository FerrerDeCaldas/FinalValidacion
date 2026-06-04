FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    mariadb-client \
    redis-tools \
    sudo \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crea usuario frappe
RUN useradd -m -s /bin/bash frappe && \
    echo "frappe ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Establece directorio de trabajo
WORKDIR /home/frappe

# Instala frappe-bench
RUN pip install --upgrade pip && \
    pip install frappe-bench

# Inicializa el bench
RUN sudo -u frappe bench init --skip-redis-config-generation frappe-bench

WORKDIR /home/frappe/frappe-bench

# Instala frappe framework
RUN sudo -u frappe bench get-app frappe --branch version-17

# Cambia permisos
RUN chown -R frappe:frappe /home/frappe

# Usuario final
USER frappe

EXPOSE 8000 8001 8002 8003

CMD ["bench", "start"]

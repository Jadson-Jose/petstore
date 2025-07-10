# ===== STAGE 1: produção (somente prod-deps) =====
FROM python:3.11-slim AS prod

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash django
USER django
WORKDIR /home/django/app

# Instala apenas libs de produção
COPY --chown=django:django requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===== STAGE 2: desenvolvimento (prod-deps + dev-deps) =====
FROM prod AS dev

# Instala libs de teste e cobertura
COPY --chown=django:django requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV PATH="/home/django/.local/bin:$PATH"

# ===== STAGE 3: final (código) =====
FROM dev AS final

# Copia a aplicação
COPY --chown=django:django . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

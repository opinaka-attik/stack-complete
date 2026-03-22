# ─────────────────────────────────────────────
# STAGE 1 : Builder (installe les dépendances)
# ─────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ─────────────────────────────────────────────
# STAGE 2 : Production (image finale, légère)
# ─────────────────────────────────────────────
FROM python:3.11-slim AS production

WORKDIR /app

# Copier uniquement les dépendances installées
COPY --from=builder /root/.local /root/.local

# Copier le code de l'application
COPY api/       ./api/
COPY postgres/  ./postgres/

# Variables d'environnement
ENV PATH=/root/.local/bin:$PATH
ENV APP_ENV=production
ENV APP_VERSION=1.0.0
ENV PYTHONPATH=/app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["python", "-m", "api.app"]
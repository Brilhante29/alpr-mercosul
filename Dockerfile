FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml requirements.txt LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --no-deps .


ENTRYPOINT ["alpr-mercosul"]
CMD ["benchmark", "--n-plates", "100", "--seed", "42", "--output", "benchmarks/results/latest.json"]

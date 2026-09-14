FROM python:3.12.14-slim-trixie@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea

RUN apt-get update && apt-get upgrade --yes && rm -rf /var/lib/apt/lists/*

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

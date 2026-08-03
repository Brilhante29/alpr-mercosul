param([switch]$SkipBuild)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $root "benchmarks/config/alpr-synthetic-v1.json"
$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
$container = "pub_alpr_mercosul_$PID"
$image = "alpr-mercosul"

Push-Location -LiteralPath $root
try {
  if (-not $SkipBuild) {
    & docker build -t $image .
    if ($LASTEXITCODE -ne 0) { throw "docker build failed with exit code $LASTEXITCODE" }
  }

  $producerArgs = @(
    "--repo", $root,
    "--project", "alpr-mercosul",
    "--benchmark-id", "alpr-ocr",
    "--image", $image,
    "--v1-result", "benchmarks/results/baseline.json",
    "--from-container", "${container}:/app/benchmarks/results/baseline.json",
    "--fixture", "src/alpr_mercosul/fixture.py",
    "--config", "benchmarks/config/alpr-synthetic-v1.json",
    "--lock", "requirements.txt",
    "--output", "benchmarks/publication/alpr-baseline-v2.json",
    "--direction", "higher_is_better",
    "--workload-version", [string]$config.workload_version,
    "--warmup-iterations", "0",
    "--concurrency", "1",
    "--runtime", "python-3.12-slim",
    "--architecture", "amd64",
    "--hardware-class", "docker-local",
    "--producer", "local",
    "--comparability-key", "alpr-ocr:$($config.workload_version):template-matching-v1:synthetic-plates:amd64",
    "--timeout-seconds", "60",
    "--",
    "docker", "run", "--name", $container, $image,
    "benchmark", "--n-plates", [string]$config.n_plates,
    "--seed", [string]$config.seed,
    "--output", "/app/benchmarks/results/baseline.json"
  )
  & python (Join-Path $PSScriptRoot "generate-publication-benchmark.py") @producerArgs
  if ($LASTEXITCODE -ne 0) {
    throw "publication benchmark producer failed with exit code $LASTEXITCODE"
  }
} finally {
  $existing = (& docker container ls -a --filter "name=^/${container}$" --format "{{.ID}}" 2>$null).Trim()
  if ($existing) { & docker container rm --force $container | Out-Null }
  Pop-Location
}

$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw 'Instala ffmpeg y añádelo a PATH.' }
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    & py -3.11 -m venv .venv
    if ($LASTEXITCODE) { throw 'No se pudo crear el entorno Python 3.11.' }
}
& .venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE) { throw 'No se pudieron instalar las dependencias.' }
& .venv\Scripts\python.exe -m pip check
if ($LASTEXITCODE) { throw 'Hay dependencias incompatibles.' }
& .venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__, '| CUDA:', torch.cuda.is_available())"
if ($LASTEXITCODE) { throw 'No se pudo cargar PyTorch.' }

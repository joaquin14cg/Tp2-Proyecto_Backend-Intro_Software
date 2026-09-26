#!/bin/bash

set -e

echo "=============================================="
echo "  Configuración del ambiente virtual - TP"
echo "=============================================="
echo ""

# -------------------------------------------------
# 1. Verificar Python
# -------------------------------------------------

if ! command -v python3 &> /dev/null; then
    echo "Python3 no está instalado. Instalando..."

    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-full python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        echo "❌ No se pudo instalar Python3 automáticamente."
        echo "Instalalo manualmente y volvé a ejecutar este script."
        exit 1
    fi
else
    echo "✓ Python3 ya está instalado: $(python3 --version)"
fi

echo ""

# -------------------------------------------------
# 2. Verificar pip
# -------------------------------------------------

if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip no está disponible."
    echo "Instalalo manualmente antes de continuar."
    exit 1
else
    echo "✓ pip disponible: $(python3 -m pip --version)"
fi

echo ""

# -------------------------------------------------
# 3. Crear ambiente virtual
# -------------------------------------------------

echo "Creando ambiente virtual..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Ambiente virtual creado"
else
    echo "✓ El ambiente virtual ya existe"
fi

echo ""

# -------------------------------------------------
# 4. Activar ambiente virtual
# -------------------------------------------------

echo "Activando ambiente virtual..."

source .venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: no se pudo activar el ambiente virtual"
    exit 1
fi

echo "✓ Ambiente virtual activado:"
echo "  $VIRTUAL_ENV"

echo ""

# -------------------------------------------------
# 5. Actualizar pip
# -------------------------------------------------

echo "Actualizando pip..."

python -m pip install --upgrade pip

echo "✓ pip actualizado"

echo ""

# -------------------------------------------------
# 6. Instalar dependencias
# -------------------------------------------------

if [ ! -f "requirements.txt" ]; then
    echo "❌ No se encontró requirements.txt"
    echo "Ejecutá este script desde la carpeta raíz del proyecto."
    exit 1
fi

echo "Instalando dependencias desde requirements.txt..."

python -m pip install -r requirements.txt

echo "✓ Dependencias instaladas"

echo ""

# -------------------------------------------------
# 7. Verificar archivo .env
# -------------------------------------------------

if [ -f ".env" ]; then
    echo "✓ Archivo .env encontrado"
else
    echo "⚠️ No se encontró el archivo .env"
    echo "   Verificá que las variables de conexión a MySQL estén configuradas."
fi

echo ""

# -------------------------------------------------
# 8. Finalización
# -------------------------------------------------

echo "=============================================="
echo "  ✓ Ambiente configurado correctamente"
echo "=============================================="
echo ""

echo "Para activar el ambiente posteriormente:"
echo "  source .venv/bin/activate"
echo ""

echo "Para desactivarlo:"
echo "  deactivate"
echo ""

echo "Para levantar MySQL con Docker:"
echo "  docker compose up -d"
echo ""

echo "Para ejecutar la aplicación:"
echo "  python app.py"
echo ""

# -------------------------------------------------
# 9. Ejecutar aplicación
# -------------------------------------------------

echo "Iniciando la aplicación..."
echo ""

python app.py
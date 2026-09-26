#!/bin/bash

set -e

echo "=============================================="
echo "   Configuración del TP - Club Deportivo"
echo "=============================================="
echo ""

# ============================================================
# 1. Python
# ============================================================

if ! command -v python3 &> /dev/null; then
    echo "Python3 no está instalado. Instalando..."

    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
else
    echo "✓ Python3 ya está instalado: $(python3 --version)"
fi

echo ""

# ============================================================
# 2. MySQL
# ============================================================

if ! command -v mysql &> /dev/null; then
    echo "MySQL no está instalado. Instalando..."

    sudo apt update
    sudo apt install -y mysql-server
else
    echo "✓ MySQL ya está instalado"
fi

echo ""

# ============================================================
# 3. Iniciar MySQL
# ============================================================

echo "Iniciando servicio MySQL..."

sudo systemctl enable mysql
sudo systemctl start mysql

echo "✓ MySQL está funcionando"
echo ""

# ============================================================
# 4. Verificar archivos del proyecto
# ============================================================

if [ ! -f "requirements.txt" ]; then
    echo "❌ No se encontró requirements.txt"
    echo "Ejecutá este script desde la carpeta raíz del proyecto."
    exit 1
fi

if [ ! -f "sql/init_db.sql" ]; then
    echo "❌ No se encontró sql/init_db.sql"
    exit 1
fi

echo "✓ Archivos del proyecto encontrados"
echo ""

# ============================================================
# 5. Crear ambiente virtual
# ============================================================

echo "Creando ambiente virtual..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Ambiente virtual creado"
else
    echo "✓ El ambiente virtual ya existe"
fi

echo ""

# ============================================================
# 6. Activar ambiente virtual
# ============================================================

source .venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ No se pudo activar el ambiente virtual"
    exit 1
fi

echo "✓ Ambiente virtual activado"
echo ""

# ============================================================
# 7. Instalar dependencias
# ============================================================

echo "Actualizando pip..."

python -m pip install --upgrade pip

echo ""
echo "Instalando dependencias..."

python -m pip install -r requirements.txt

echo "✓ Dependencias instaladas"
echo ""

# ============================================================
# 8. Crear .env
# ============================================================

if [ ! -f ".env" ]; then

    echo "No existe .env. Creándolo..."

    cat > .env <<'EOF'
DB_HOST=localhost
DB_PORT=3306
DB_NAME=club_deportivo
DB_USER=club_admin
DB_PASSWORD=lanzillotta
EOF

    echo "✓ .env creado"

else

    echo "✓ .env ya existe"

fi

echo ""

# ============================================================
# 9. Inicializar base de datos
# ============================================================

echo "Inicializando base de datos..."

sudo mysql < sql/init_db.sql

echo "✓ Base de datos configurada"
echo ""

# ============================================================
# 10. Finalización
# ============================================================

echo "=============================================="
echo "  ✓ TP configurado correctamente"
echo "=============================================="
echo ""

echo "Para activar el ambiente posteriormente:"
echo "  source .venv/bin/activate"
echo ""

echo "Para ejecutar el TP:"
echo "  python app.py"
echo ""

echo "=============================================="
echo ""

# ============================================================
# 11. Ejecutar aplicación
# ============================================================

echo "Iniciando aplicación..."
echo ""

python app.py
#!/bin/bash

set -e

echo "=============================================="
echo "   Configuración del TP - Club Deportivo"
echo "=============================================="
echo ""

# ============================================================
# 1. Verificar que estamos en la raíz del proyecto
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
# 2. Python
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
# 3. MySQL
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
# 4. Iniciar MySQL
# ============================================================

echo "Iniciando servicio MySQL..."

sudo systemctl enable mysql
sudo systemctl start mysql

echo "✓ MySQL está funcionando"
echo ""

# ============================================================
# 5. Configurar MySQL
# ============================================================

echo "Configurando base de datos y usuario..."

sudo mysql <<'SQL'

-- ============================================================
-- Crear base de datos
-- ============================================================

CREATE DATABASE IF NOT EXISTS club_deportivo
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- ============================================================
-- Crear usuario del proyecto
-- ============================================================

CREATE USER IF NOT EXISTS 'club_user'@'localhost'
    IDENTIFIED BY 'ClubPassword123!';

ALTER USER 'club_user'@'localhost'
    IDENTIFIED BY 'ClubPassword123!';

-- ============================================================
-- Dar permisos al usuario sobre la base del proyecto
-- ============================================================

GRANT ALL PRIVILEGES ON club_deportivo.*
    TO 'club_user'@'localhost';

FLUSH PRIVILEGES;

SQL

echo "✓ Base de datos 'club_deportivo' creada"
echo "✓ Usuario 'club_user' configurado"
echo "✓ Permisos configurados"
echo ""

# ============================================================
# 6. Inicializar tablas
# ============================================================

echo "Inicializando tablas de la base de datos..."

sudo mysql club_deportivo < sql/init_db.sql

echo "✓ Base de datos inicializada"
echo ""

# ============================================================
# 7. Crear archivo .env
# ============================================================

echo "Configurando variables de entorno..."

cat > .env <<'EOF'
DB_HOST=localhost
DB_PORT=3306
DB_NAME=club_deportivo
DB_USER=club_user
DB_PASSWORD=ClubPassword123!
EOF

echo "✓ Archivo .env configurado"
echo ""

# ============================================================
# 8. Crear ambiente virtual
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
# 9. Activar ambiente virtual
# ============================================================

source .venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ No se pudo activar el ambiente virtual"
    exit 1
fi

echo "✓ Ambiente virtual activado"
echo ""

# ============================================================
# 10. Instalar dependencias
# ============================================================

echo "Actualizando pip..."

python -m pip install --upgrade pip

echo ""
echo "Instalando dependencias del proyecto..."

python -m pip install -r requirements.txt

echo "✓ Dependencias instaladas"
echo ""

# ============================================================
# 11. Verificar conexión con la base de datos
# ============================================================

echo "Verificando conexión con MySQL..."

if mysql \
    -h localhost \
    -P 3306 \
    -u club_user \
    -p'ClubPassword123!' \
    -e "USE club_deportivo;" &> /dev/null
then
    echo "✓ Conexión con club_deportivo exitosa"
else
    echo "❌ No se pudo conectar con la base de datos"
    exit 1
fi

echo ""

# ============================================================
# 12. Finalización
# ============================================================

echo "=============================================="
echo "  ✓ TP configurado correctamente"
echo "=============================================="
echo ""

echo "Base de datos:"
echo "  club_deportivo"
echo ""

echo "Usuario:"
echo "  club_user"
echo ""

echo "Puerto:"
echo "  3306"
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
# 13. Ejecutar aplicación
# ============================================================

echo "Iniciando aplicación..."
echo ""

python app.py
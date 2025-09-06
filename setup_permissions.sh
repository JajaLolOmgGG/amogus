#!/bin/bash

echo "🔧 Configurando permisos para ejecutables..."

# Función para dar permisos y mostrar resultado
give_permissions() {
    local file="$1"
    if [ -f "$file" ]; then
        chmod +x "$file"
        if [ $? -eq 0 ]; then
            echo "✅ Permisos otorgados a: $file"
        else
            echo "❌ Error al dar permisos a: $file"
        fi
    else
        echo "⚠️  Archivo no encontrado: $file"
    fi
}

# Lista de archivos ejecutables comunes
executables=(
    "./playit-linux-amd64"
    "./Impostor.Server"
    "./server"
    "./run.sh"
    "./start.sh"
)

# Dar permisos a archivos específicos
for exe in "${executables[@]}"; do
    give_permissions "$exe"
done

# Buscar otros ejecutables potenciales
echo ""
echo "🔍 Buscando otros ejecutables..."

# Archivos sin extensión que podrían ser ejecutables
find . -maxdepth 2 -type f ! -name "*.py" ! -name "*.txt" ! -name "*.md" ! -name "*.json" ! -name "*.cfg" ! -name "*.conf" ! -name "*.log" -executable 2>/dev/null | while read -r file; do
    if [ ! -x "$file" ]; then
        give_permissions "$file"
    fi
done

# Archivos .Server específicamente
find . -name "*.Server" -type f | while read -r file; do
    give_permissions "$file"
done

echo ""
echo "📋 Resumen de archivos ejecutables:"
echo "=================================="
ls -la | grep '^-..x' | while read -r line; do
    filename=$(echo "$line" | awk '{print $NF}')
    echo "✅ $filename"
done

echo ""
echo "🎯 Configuración de permisos completada!"
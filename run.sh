# Debian (Linux) Script

# Eliminar la carpeta 'build' solo si existe
if [ -d "build" ]; then
    echo "La carpeta 'build' existe. Eliminando..."
    rm -rf build
    echo "La carpeta 'build' ha sido eliminada."
fi

# Crear la carpeta 'build' y navegar a ella
mkdir -p build && cd build

# Configurar con CMake
cmake ..

# Compilar con make
make

# Ejecutar el programa
./TFLiteMoveNet

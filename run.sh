# Debian (Linux) Script

# Exist main.py in the current directory
if [ ! -f "main.py" ]; then
    echo "Error: No se encontró el archivo main.py en el directorio actual."
    exit 1
fi

# Exist detection folder in the current directory
if [ ! -d "detection" ]; then
    echo "Error: No se encontró la subcarpeta 'detection'."
    exit 1
fi

# Exist .mp4 files in the detection folder
mp4_files=$(find detection -type f -name "*.mp4")
# Verificar si no se encontraron archivos mp4
if [ -z "$mp4_files" ]; then
    echo "No se encontraron archivos .mp4 en la subcarpeta 'detection'. Descargando videos..."
    python3 utils/download_vid.py
    exit 0
fi

if [ "$1" = "cpp" ]; then

    echo "Compilando el modelo TFLite en C++..."

    # Download TFLite template project if not exists
    if [ ! -d "tflite" ]; then
        echo "Descargando el modelo TFLite..."
        git clone https://github.com/karthickai/tflite
        echo "Clone repository 'tflite' has been downloaded"
    fi

    # Move to the tflite folder
    cd tflite || exit

    # Move to the 04_Linux_Installation folder
    cd 04_Linux_Installation || exit

    # Delete CMakeLists.txt and main.cpp
    rm -f CMakeLists.txt main.cpp

    # Copy CMakeLists.txt from root directory
    cp ../../CMakeLists.txt .
    
    # Copy movenet_cpp.cpp from detection/movenet.cpp
    cp ../../detection/movenet.cpp .

    # Copy model.tflite from detection/model.tflite
    cp ../../resources/models/model.tflite .

    # Copy sentadilla.mp4 from detection/sentadilla.mp4
    cp ../../detection/sentadilla.mp4 .

    echo "Archivos CMakeLists.txt han sido actualizados en la carpeta '04_Linux_Installation'"

    # Eliminar la carpeta 'build' solo si existe
    if [ -d "build" ]; then
        echo "La carpeta 'build' existe. Eliminando..."
        rm -rf build
        echo "La carpeta 'build' ha sido eliminada."
    fi

    # Crear la carpeta 'build' y navegar a ella
    mkdir build && cd build

    # Configurar con CMake
    cmake ..

    # Compilar con make
    make

    # Ejecutar el programa
    # ./TFLiteMoveNet
fi



echo "¡Todo parece estar en orden!"

# Run the main.py script
python3 main.py

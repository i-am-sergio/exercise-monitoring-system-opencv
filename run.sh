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
if [ -z "$mp4_files" ]; then
    echo "Error: No se encontraron archivos .mp4 en la subcarpeta 'detection'."
    exit 1
fi

echo "¡Todo parece estar en orden!"

# Run the main.py script
python3 main.py

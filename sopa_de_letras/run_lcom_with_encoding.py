import subprocess

# Ruta al archivo que deseas analizar
file_path = "Sopa.py"

# Ejecutar el comando `lcom` especificando la codificación
command = ["lcom", file_path]
try:
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    print("Salida estándar:")
    print(result.stdout)
    print("Error estándar:")
    print(result.stderr)
except Exception as e:
    print("Error al ejecutar el comando:", e)

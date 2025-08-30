"""
Script para compilar la aplicación a un archivo .exe
Requiere PyInstaller: pip install pyinstaller
"""

import os
import subprocess
import shutil

def build_exe():
    """Compila la aplicación a .exe"""
    
    print("🔨 Compilando aplicación...")
    
    # Comando para PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo .exe
        "--windowed",                   # Sin consola (solo ventana gráfica)
        "--name=MiApp",                # Nombre del ejecutable
        "--icon=icon.ico",             # Icono (opcional, crear un icon.ico)
        "--add-data=version.txt;.",    # Incluir archivo de versión
        "main.py"
    ]
    
    # Crear archivo de versión inicial si no existe
    if not os.path.exists("version.txt"):
        with open("version.txt", "w") as f:
            f.write("1.0.0")
    
    # Ejecutar PyInstaller
    try:
        subprocess.run(cmd, check=True)
        print("✅ Compilación exitosa!")
        
        # Mover el .exe a la carpeta raíz
        if os.path.exists("dist/MiApp.exe"):
            if os.path.exists("MiApp.exe"):
                os.remove("MiApp.exe")
            shutil.move("dist/MiApp.exe", "MiApp.exe")
            print("📁 Archivo MiApp.exe creado")
            
        # Limpiar archivos temporales
        cleanup()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la compilación: {e}")
        return False
    
    return True

def cleanup():
    """Limpia archivos temporales de la compilación"""
    dirs_to_remove = ["build", "dist", "__pycache__"]
    files_to_remove = ["MiApp.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
    
    print("🧹 Archivos temporales eliminados")

def create_icon():
    """Crea un icono básico (opcional)"""
    # Este es un placeholder - puedes reemplazar con tu propio icono
    print("💡 Tip: Agrega un archivo 'icon.ico' para personalizar el icono")

if __name__ == "__main__":
    print("🚀 Iniciando proceso de compilación...")
    
    # Verificar que PyInstaller esté instalado
    try:
        subprocess.run(["pyinstaller", "--version"], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller no está instalado")
        print("Instálalo con: pip install pyinstaller")
        exit(1)
    
    # Compilar
    if build_exe():
        print("\n🎉 ¡Aplicación compilada exitosamente!")
        print("📦 Archivo listo para distribución: MiApp.exe")
        print("\n📋 Próximos pasos:")
        print("1. Sube 'main.py' y 'config.json' a tu repositorio GitHub")
        print("2. Actualiza las URLs en main.py con tu repositorio")
        print("3. Distribuye 'MiApp.exe' a tus usuarios")
    else:
        print("❌ Falló la compilación")
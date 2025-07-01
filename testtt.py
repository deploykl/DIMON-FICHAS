import os
import re
import shutil

def limpiar_nombre_archivo(nombre):
    # Patrones a eliminar (expresiones regulares)
    patrones = [
        r'\[Official Music Video\]',
        r'\[Official Video\]',
        r'\(Official Music Video\)',
        r'\(Official Video\)',
        r'Sub\. Español(\(.*?\))?',
        r'\(MP3_\d+K\)',
        r'\(\d+ ?kbps\)',
        r'\(\d+ ?k\)',
        r'\(Lyric Video\)',
        r'\(Lyrics\)',
        r'\(Audio\)',
        r'\(Video Oficial\)',
        r'\[Video Oficial\]',
        r'\(Official Audio\)',
        r'\[Official Audio\]',
        r'\(Official Lyric Video\)',
        r'\[Official Lyric Video\]',
        r'\(\d{3,4}p\)',  # Resoluciones como (720p) o (1080p)
        r'\[.*?\]',  # Cualquier texto entre corchetes
        r'\(.*?\)',  # Cualquier texto entre paréntesis
    ]
    
    for patron in patrones:
        nombre = re.sub(patron, '', nombre, flags=re.IGNORECASE)
    
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    nombre = re.sub(r'^\s*-\s*|\s*-\s*$', '', nombre)
    nombre = re.sub(r'\s*-\s*', ' - ', nombre)
    
    return nombre

def crear_carpeta_salida():
    # Crear ruta en D:\ con nombre fijo
    nombre_carpeta = "Musica_Limpia"
    ruta_salida = os.path.join("D:\\", nombre_carpeta)
    
    # Crear la carpeta si no existe
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    
    return ruta_salida

def procesar_y_copiar():
    # Ruta de origen (raíz de E:)
    ruta_origen = "E:\\"
    
    # Verificar si el disco E: existe
    if not os.path.exists(ruta_origen):
        print("\nERROR: No se encontró el disco E:. ¿Está conectado?")
        return
    
    # Verificar disco D:
    if not os.path.exists("D:\\"):
        print("\nERROR: No se encontró el disco D:. ¿Está conectado?")
        return
    
    ruta_salida = crear_carpeta_salida()
    print(f"\nCopiando archivos limpios a: {ruta_salida}\n")
    
    # Procesar solo archivos en la raíz de E:
    for nombre_archivo in os.listdir(ruta_origen):
        ruta_completa_origen = os.path.join(ruta_origen, nombre_archivo)
        
        if os.path.isfile(ruta_completa_origen):
            # Verificar si es archivo de música por extensión
            if nombre_archivo.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.aac')):
                nombre_base, extension = os.path.splitext(nombre_archivo)
                nombre_limpio = limpiar_nombre_archivo(nombre_base)
                nuevo_nombre = f"{nombre_limpio}{extension}"
                ruta_destino = os.path.join(ruta_salida, nuevo_nombre)
                
                try:
                    # Copiar el archivo con el nuevo nombre
                    shutil.copy2(ruta_completa_origen, ruta_destino)
                    print(f"Copiado: {nombre_archivo.ljust(60)} -> {nuevo_nombre}")
                except Exception as e:
                    print(f"Error al copiar {nombre_archivo}: {e}")

if __name__ == "__main__":
    print("=== LIMPIADOR DE NOMBRES DE ARCHIVOS DE MÚSICA ===")
    print("Este script:")
    print("1. Buscará archivos de música en la raíz de E:\\")
    print("2. Creará una carpeta 'Musica_Limpia' en D:\\")
    print("3. Copiará los archivos con nombres limpios\n")
    
    input("Presiona Enter para comenzar...")
    
    procesar_y_copiar()
    
    print("\nProceso completado. Presiona Enter para salir.")
    input()
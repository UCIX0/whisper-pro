#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
from colorama import init, Fore, Style
from faster_whisper import WhisperModel
from tqdm import tqdm

# Inicializar colores. En Linux 'init()' suele ser automático, pero lo dejamos por seguridad.
init(autoreset=True)


def log_info(msg):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")


def log_success(msg):
    print(f"{Fore.GREEN}[ÉXITO]{Style.RESET_ALL} {msg}")


def log_warning(msg):
    print(f"{Fore.YELLOW}[AVISO]{Style.RESET_ALL} {msg}")


def log_error(msg):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")


def obtener_duracion_ffmpeg(ruta_archivo):
    """
    Obtiene la duración total del archivo usando ffprobe.
    """
    try:
        # En Linux, ffprobe debe estar instalado en el sistema (pacman -S ffmpeg)
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            ruta_archivo
        ]
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        data = json.loads(result.stdout)
        duration = float(data['format']['duration'])
        return duration
    except Exception as e:
        # Si falla, no rompemos el programa, solo no mostramos barra precisa
        return None


def limpiar_ruta(ruta):
    """
    Limpia las rutas de Linux/Windows.
    Linux a veces usa comillas simples 'ruta' al arrastrar, 
    y a veces escapa espacios con backslash si no usa comillas.
    """
    ruta = ruta.strip()  # Quitar espacios alrededor
    ruta = ruta.strip('"')  # Quitar comillas dobles (común en Windows)
    ruta = ruta.strip("'")  # Quitar comillas simples (común en Linux)
    # Nota: Si tu terminal escapa espacios (ej: video\ vacacion.mp4) sin comillas,
    # python lo suele leer bien, pero si tienes problemas, avísame.
    return ruta


def transcribir_archivo(ruta_entrada):
    # 1. Limpieza de Ruta
    ruta_entrada = limpiar_ruta(ruta_entrada)

    if not os.path.exists(ruta_entrada):
        log_error(
            f"El archivo no existe o la ruta es incorrecta: {ruta_entrada}")
        return

    nombre_base = os.path.splitext(os.path.basename(ruta_entrada))[0]
    directorio = os.path.dirname(ruta_entrada)
    ruta_salida = os.path.join(directorio, f"{nombre_base}.txt")

    log_info(f"Archivo detectado: {nombre_base}")

    # 2. Obtener duración
    duracion_total = obtener_duracion_ffmpeg(ruta_entrada)

    # 3. Cargar Modelo
    try:
        log_info("Cargando modelo 'large-v3' en GPU (CUDA)...")
        start_load = time.time()

        # Modificado para descargar automáticamente si no existe la carpeta
        model = WhisperModel("large-v3", device="cuda",
                             compute_type="float16", download_root="./modelo_whisper")

        load_time = time.time() - start_load
        log_success(f"Modelo cargado en {load_time:.2f} segundos.")
    except Exception as e:
        log_error(
            f"Fallo al cargar el modelo. Verifica tus drivers NVIDIA: {e}")
        return

    # 4. Transcripción
    log_info("Iniciando transcripción...")
    texto_completo = []

    try:
        segments, info = model.transcribe(
            ruta_entrada,
            beam_size=5,
            language="es",
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        log_info(
            f"Idioma: {info.language.upper()} (Probabilidad: {info.language_probability:.2%})")

        with tqdm(total=duracion_total, unit="seg", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} seg") as pbar:
            for segment in segments:
                texto_completo.append(segment.text)

                avance = segment.end - pbar.n
                if avance > 0:
                    pbar.update(avance)

        # 5. Guardar
        contenido_final = "\n".join(texto_completo)
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(contenido_final)

        print("\n" + "="*50)
        log_success(f"Transcripción guardada en: {ruta_salida}")
        print("="*50 + "\n")

    except Exception as e:
        log_error(f"Error durante la transcripción: {e}")


if __name__ == "__main__":
    # Limpia pantalla compatible con Linux/Mac/Windows
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.MAGENTA}--- TRANSCRIPTOR WHISPER LINUX (RTX 4070) ---{Style.RESET_ALL}")

    while True:
        try:
            path = input(
                "Arrastra el archivo aquí o pega la ruta ('exit' para salir): ")
            if path.lower() in ["salir", "exit"]:
                break
            if path.strip() == "":
                continue

            transcribir_archivo(path)
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

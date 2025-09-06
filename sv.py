import os
import subprocess
from multiprocessing import Process
import time
import logging
import uvicorn
from fastapi import FastAPI

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def run_playit():
    """Ejecuta playit-linux-amd64"""
    try:
        logger.info("🚀 [PLAYIT] Iniciando playit-linux-amd64...")
        playit_path = "./playit-linux-amd64"
        
        if os.path.exists(playit_path):
            # Dar permisos de ejecución automáticamente
            os.chmod(playit_path, 0o755)
            logger.info(f"✅ [PLAYIT] Permisos otorgados a {playit_path}")
            
            # Ejecuta y muestra la salida en tiempo real
            process = subprocess.Popen(
                playit_path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Lee la salida línea por línea
            for line in process.stdout:
                print(f"[PLAYIT] {line.strip()}")
                
            process.wait()
        else:
            logger.error(f"❌ [PLAYIT] {playit_path} no encontrado")
    except Exception as e:
        logger.error(f"❌ [PLAYIT] Error: {e}")

def run_impostor_server():
    """Ejecuta Impostor.Server"""
    try:
        logger.info("🎮 [IMPOSTOR] Iniciando Impostor.Server...")
        impostor_path = "./Impostor.Server"
        
        if os.path.exists(impostor_path):
            # Dar permisos de ejecución automáticamente
            os.chmod(impostor_path, 0o755)
            logger.info(f"✅ [IMPOSTOR] Permisos otorgados a {impostor_path}")
            
            # Ejecuta y muestra la salida en tiempo real
            process = subprocess.Popen(
                impostor_path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Lee la salida línea por línea
            for line in process.stdout:
                print(f"[IMPOSTOR] {line.strip()}")
                
            process.wait()
        else:
            logger.error(f"❌ [IMPOSTOR] {impostor_path} no encontrado")
    except Exception as e:
        logger.error(f"❌ [IMPOSTOR] Error: {e}")

def start_services():
    """Inicia los servicios en procesos separados"""
    # Crear procesos separados para cada servicio
    playit_process = Process(target=run_playit)
    impostor_process = Process(target=run_impostor_server)
    
    # Iniciar procesos
    playit_process.start()
    time.sleep(2)  # Pequeña pausa entre inicios
    impostor_process.start()
    
    logger.info("Servicios iniciados en procesos separados")
    return playit_process, impostor_process

@app.get("/")
async def read_root():
    return {
        "message": "Hello World",
        "status": "running",
        "services": ["playit-linux-amd64", "Impostor.Server"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "port": 7860}

@app.get("/processes")
async def check_processes():
    """Endpoint para verificar si los procesos están corriendo"""
    playit_running = any("playit" in str(p.info['cmdline']) for p in psutil.process_iter(['pid', 'cmdline']) if p.info['cmdline'])
    impostor_running = any("Impostor" in str(p.info['cmdline']) for p in psutil.process_iter(['pid', 'cmdline']) if p.info['cmdline'])
    
    return {
        "playit_running": playit_running,
        "impostor_running": impostor_running
    }

if __name__ == "__main__":
    logger.info("Iniciando aplicación...")
    
    # Iniciar servicios
    processes = start_services()
    
    # Iniciar FastAPI
    try:
        uvicorn.run(app, host="0.0.0.0", port=7860)
    except KeyboardInterrupt:
        logger.info("Deteniendo aplicación...")
        # Terminar procesos al salir
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
        logger.info("Aplicación detenida")

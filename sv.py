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
    """Ejecuta hmm"""
    try:
        logger.info("🚀 [HMM] Iniciando hmm...")
        hmm_path = "./hmm"
        
        if os.path.exists(hmm_path):
            logger.info(f"✅ [HMM] Archivo encontrado: {hmm_path}")
            
            # Ejecuta directamente (permisos ya dados en Dockerfile)
            process = subprocess.Popen(
                hmm_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Lee la salida línea por línea
            for line in process.stdout:
                print(f"[HMM] {line.strip()}")
                
            process.wait()
        else:
            logger.error(f"❌ [HMM] {hmm_path} no encontrado")
            # Lista archivos para debugging
            files = os.listdir('.')
            logger.info(f"Archivos disponibles: {files}")
    except Exception as e:
        logger.error(f"❌ [HMM] Error: {e}")

def run_impostor_server():
    """Ejecuta Impostor.Server"""
    try:
        logger.info("🎮 [IMPOSTOR] Iniciando Impostor.Server...")
        impostor_path = "./Impostor.Server"
        
        if os.path.exists(impostor_path):
            logger.info(f"✅ [IMPOSTOR] Archivo encontrado: {impostor_path}")
            
            # Ejecuta directamente (permisos ya dados en Dockerfile)
            process = subprocess.Popen(
                impostor_path,
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
            # Lista archivos para debugging
            files = os.listdir('.')
            logger.info(f"Archivos disponibles: {files}")
    except Exception as e:
        logger.error(f"❌ [IMPOSTOR] Error: {e}")

def start_services():
    """Inicia los servicios en procesos separados"""
    # Crear procesos separados para cada servicio
    hmm_process = Process(target=run_playit)
    impostor_process = Process(target=run_impostor_server)
    
    # Iniciar procesos
    hmm_process.start()
    time.sleep(2)  # Pequeña pausa entre inicios
    impostor_process.start()
    
    logger.info("Servicios iniciados en procesos separados")
    return hmm_process, impostor_process

@app.get("/")
async def read_root():
    return {
        "message": "Hello World",
        "status": "running",
        "services": ["hmm", "Impostor.Server"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "port": 7860}

@app.get("/files")
async def list_files():
    """Lista los archivos en el directorio actual"""
    try:
        files = []
        for item in os.listdir('.'):
            stat = os.stat(item)
            files.append({
                "name": item,
                "is_executable": os.access(item, os.X_OK),
                "permissions": oct(stat.st_mode)[-3:],
                "size": stat.st_size
            })
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

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

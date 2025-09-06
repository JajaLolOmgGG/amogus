import os
import subprocess
from multiprocessing import Process
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# No Rtmp or Ffmpeg related variables

def stream_video():
    subprocess.run("./Impostor.Server", shell=True)
    subprocess.run("./hmm", shell=True)

def start_video_streaming():
    video_process = Process(target=stream_video)
    video_process.start()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    start_video_streaming()
    uvicorn.run(app, host="0.0.0.0", port=7860)


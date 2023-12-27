from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import os
import zipfile
import asyncio
import uuid
from typing import List

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store WebSocket connections
websocket_connections = {}

def get_zip_filename():
    current_directory = os.getcwd()
    parent_directory = os.path.join(current_directory, os.pardir)
    zipped_directory = os.path.join(parent_directory, "zipped")
    if not os.path.exists(zipped_directory):
        os.makedirs(zipped_directory)
    path = os.path.join(zipped_directory, f"archive_{uuid.uuid4().hex}.zip")
    return path

async def zip_files(files: List[UploadFile], output_zip_path: str):
    with zipfile.ZipFile(output_zip_path, 'w') as zip_file:
        for file in files:
            contents = await file.read()  # Read the contents of the UploadFile
            arcname = os.path.basename(file.filename)
            zip_file.writestr(arcname, contents)

async def send_progress(websocket, progress):
    await websocket.send_text(progress)

@app.post("/zip-files/")
async def zip_files_endpoint(files: List[UploadFile] = File(...)):
    process_id = uuid.uuid4().hex
    output_zip_path = get_zip_filename()
    
    await zip_files(files, output_zip_path)

    return {"process_id": process_id, "message": "Zipping process completed"}

@app.websocket("/ws/{process_id}")
async def websocket_endpoint(websocket: WebSocket, process_id: str):
    await websocket.accept()
    try:
        websocket_connections[process_id] = websocket
        await send_progress(websocket, "100% - Zipping process completed")

    except WebSocketDisconnect:
        del websocket_connections[process_id]
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1" , port="5050")

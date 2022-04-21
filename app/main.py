from typing import List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from . import schemas, utils, connection_manager
from fastapi.encoders import jsonable_encoder

app = FastAPI()

manager = connection_manager.ConnectionManager()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/productionplan", response_model=List[schemas.PowerplantResult])
async def calculate_power_for_each_of_powerplants(
        payload: schemas.Payload,
    ):
    
    utils.sort_powerplants_by_merit_order(payload=payload)
    utils.handle_wind_in_pmax(payload=payload)
    
    loaded_energy, array_powerplant_result = utils.load_energy_by_backtraking(total_load=payload.load, powerplants=payload.powerplants)
    
    if (loaded_energy != payload.load):
        raise HTTPException(status_code=500, detail="Could not validate payload")
    
    await manager.broadcast(str(jsonable_encoder(array_powerplant_result))) #WEBSOCKET

    return array_powerplant_result


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

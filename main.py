from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class SensorData(BaseModel):
    device: str
    status: str
    sensorReadings: dict

@app.post("/post-sensor-data")
async def receive_data(data: SensorData):
    try:
        # Process your data here
        print("Received data:", data)
        return {"message": "Data received successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
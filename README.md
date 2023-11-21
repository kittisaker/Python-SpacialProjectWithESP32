# Python-SpacialProjectWithESP32 : Chapter-1 Basic FastAPI application

## Example : FastAPI application
```shell
pip install fastapi uvicorn
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

```shell
uvicorn main:app --reload
```

##  Using FastAPI to receive data from your ESP32
ESP32:
```cpp
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Kittisaker";
const char* password = "87654321";
const char* serverName = "http://192.168.136.96:8000/post-sensor-data";

void setup() {
    Serial.begin(115200);
    randomSeed(analogRead(0));

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
}

void loop() {
  float value1 = random(-55, 151);
  float value2 = random(0, 101);
  float value3 = random(885, 3249) / 100.0;
  float value4 = random(0, 360);
  float value5 = random(1, 201);

    StaticJsonDocument<256> doc;
    doc["device"] = "ESP32";
    doc["status"] = "active";

    JsonObject sensorReadings = doc.createNestedObject("sensorReadings");
    sensorReadings["temperature"] = value1;
    sensorReadings["humidity"] = value2;
    sensorReadings["barometric_pressure"] = value3;
    sensorReadings["wind_direction"] = value4;
    sensorReadings["wind_speed"] = value5;

    String output;
    serializeJson(doc, output);

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverName);
        http.addHeader("Content-Type", "application/json");
        
        int httpResponseCode = http.POST(output);

        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(response);
        } else {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
        }
        http.end();
    } else {
        Serial.println("WiFi Disconnected");
    }

    delay(10000);
}
```

Python :
```python
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
```

```shell
python main.py
```

```shell
Received data: device='ESP32' status='active' sensorReadings={'temperature': -9, 'humidity': 64, 'barometric_pressure': 31.04999924, 'wind_direction': 218, 'wind_speed': 166}
INFO:     192.168.136.47:52703 - "POST /post-sensor-data HTTP/1.1" 200 OK
```
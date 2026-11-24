from pydantic import BaseModel;

import json;

from pathlib import Path;

SERVICE_DDBB_PATH = Path(__file__).resolve().parent.parent / "ddbb" / "services_ddbb.json";

class Service(BaseModel):
    """Catalog service schema shared across mobile and desktop APIs."""

    id: int;
    name: str;
    description: str = "";
    price: float;
    is_active: bool = True;

def readServices() -> list:
    raw = SERVICE_DDBB_PATH.read_text(encoding="utf-8").strip();
    data = json.loads(raw) if raw else {"services": []};
            
    return [Service.model_validate(item) for item in data["services"]];

def insertService(s: Service) -> None:
    raw = SERVICE_DDBB_PATH.read_text(encoding="utf-8").strip();
    data = json.loads(raw) if raw else {"services": []};
    data.setdefault("services", []).append(s.model_dump());

    SERVICE_DDBB_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8");

def updateService(id: int, s: Service) -> None:
    raw = SERVICE_DDBB_PATH.read_text(encoding="utf-8").strip();
    
    if not raw or raw == '{}':
        raise ValueError("No DDBB found");
    
    data = json.loads(raw);
    
    services = data["services"];
    
    matches = [i for i, item in enumerate(services) if item["id"] == id];
    
    if not matches:
        raise ValueError(f"No serivce with id {id}");
    
    if len(matches) > 1:
        raise ValueError(f"Multiple services have id {id}");
    
    services[matches[0]] = s.model_dump();
    SERVICE_DDBB_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8");

def deleteService(id: int) -> None:
    raw = SERVICE_DDBB_PATH.read_text(encoding="utf-8").strip();
    
    if not raw or raw == '{}':
        raise ValueError("No DDBB found");
    
    data = json.loads(raw);

    services = data["services"];
    
    matches = [i for i, item in enumerate(services) if item["id"] == id];
    
    if not matches:
        raise ValueError(f"No service with id {id}");
    
    if len(matches) > 1:
        raise ValueError(f"Multiple services have id {id}");

    del services[matches[0]];
    SERVICE_DDBB_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8");
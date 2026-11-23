from pydantic import BaseModel;

import json;

from pathlib import Path;

VINYL_DDBB_PATH = Path(__file__).resolve().parent.parent / "ddbb" / "vinyl_ddbb.json"

class Vinyl(BaseModel):
    id:     int;
    name:   str;
    author: str;
    price:  float;

def readVinyls():
    data = json.loads(VINYL_DDBB_PATH.read_text(encoding="utf-8"));
            
    return [Vinyl.model_validate(item) for item in data["vinyls"]];

def insertVinyl(v: Vinyl):
    data = json.loads(VINYL_DDBB_PATH.read_text(encoding="utf-8") or '{}');
    data.setdefault("vinyls", []).append(v.model_dump());

    VINYL_DDBB_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8");

def updateVinyl(id: int, v: Vinyl):
    data = json.loads(VINYL_DDBB_PATH.read_text(encoding="utf-8"));
    vinyls = data["vinyls"];

    matches = [i for i, item in enumerate(vinyls) if item["id"] == id];

    if not matches:
        raise ValueError(f"No vinyl with id {id}");

    if len(matches) > 1:
        raise ValueError(f"Multiple vinyls have id {id}");

    vinyls[matches[0]] = v.model_dump();
    VINYL_DDBB_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8");
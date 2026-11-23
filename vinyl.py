from pydantic import BaseModel;

import json;

from pathlib import Path;

VINYL_DDBB_PATH = Path("../ddbb").with_name("vinyl_ddbb.json");

class Vinyl(BaseModel):
    id:     int;
    name:   str;
    author: str;
    price:  float;

def readVinyls():
    content = VINYL_DDBB_PATH.read_text(encoding="utf-8");
            
    if not content.strip():
        return [];
            
    return [Vinyl.model_validate(item) for item in json.loads(content)];

def insertVinyl(v: Vinyl):
    data = json.loads(VINYL_DDBB_PATH.read_text(encoding="utf-8") or '{}');
    data.setdefault("vinyls", []).append(v.model_dump());

    VINYL_DDBB_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8");

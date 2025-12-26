#Evitar posteos consecutivos para evitar posts vacíos contenido corto o largo, títulos basura spam
import time
from fastapi import Request, HTTPException

RATE_LIMITS = 5 #request
WINDOW = 60 #segundos

_clients: dict[str, list[float]] = {}

#5 requests cada 60 segundos por cliente
async def rate_limits_posts(request: Request):
    ip = request.client.host
    anon_key = request.cookies.get("anon_key", "no-key")

    key = f"{ip}:{anon_key}" #identificar al usuario por ip y por anon key
    now = time.time() #para obtener el timestamp actual
    timestamps = _clients.get(key, [])
    #elmiminar rquest viejos    
    timestamps = [ t for t in timestamps if now -t < WINDOW]

    if len(timestamps) >= RATE_LIMITS:
        raise HTTPException(status_code=429, detail="Demasiadas publicaciones. Esperá un momento.")
    
    timestamps.append(now)
    _clients[key] = timestamps
      

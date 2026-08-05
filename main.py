import os
from fastapi import FastAPI, Request, Response
import uvicorn
import httpx

app = FastAPI()

# URL de destination (ton VPS ou ton service local)
TARGET_URL = "http://simon.benbilal237free.xyz"

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy(request: Request, path_name: str):
    async with httpx.AsyncClient(timeout=60.0) as client:
        url = f"{TARGET_URL}/{path_name}"
        headers = dict(request.headers)
        headers.pop("host", None) # Nettoie le host pour éviter les conflits d'URL
        
        body = await request.body()
        
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=dict(resp.headers)
            )
        except Exception as e:
            return Response(content=str(e), status_code=502)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

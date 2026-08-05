import httpx

TARGET = "http://simon.benbilal237free.xyz:80"

async def app(scope, receive, send):
    if scope["type"] != "http":
        return

    async with httpx.AsyncClient() as client:
        url = TARGET + scope["path"]
        if scope.get("query_string"):
            url += "?" + scope["query_string"].decode()

        headers = dict(scope["headers"])
        headers[b"host"] = b"simon.benbilal237free.xyz"

        req = client.build_request(
            method=scope["method"],
            url=url,
            headers=headers,
            content=request_body_generator(receive)
        )

        res = await client.send(req, stream=True)

        await send({
            "type": "http.response.start",
            "status": res.status_code,
            "headers": [(k.encode(), v.encode()) for k, v in res.headers.raw]
        })

        async for chunk in res.aiter_bytes():
            await send({
                "type": "http.response.body",
                "body": chunk,
                "more_body": True
            })

        await send({"type": "http.response.body", "body": b"", "more_body": False})

async def request_body_generator(receive):
    while True:
        message = await receive()
        if message["type"] == "http.request":
            yield message.get("body", b"")
            if not message.get("more_body", False):
                break

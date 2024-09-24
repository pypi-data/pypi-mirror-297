from typing import Any, Awaitable, Callable, MutableMapping

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]


class Obelisk:
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:
        if scope["type"] == "lifespan":
            await self.handle_lifespan(scope, receive, send)
        elif scope["type"] == "http":
            await self.handle_http(scope, receive, send)

    async def handle_lifespan(self, scope: Scope, receive: Receive, send: Send):
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                break

    async def handle_http(self, scope: Scope, receive: Receive, send: Send):
        response_msg = {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
        await send(response_msg)

        response_msg = {
            "type": "http.response.body",
            "body": b"hello world!",
            "more_body": False,
        }
        await send(response_msg)

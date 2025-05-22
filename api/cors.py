from fastapi.middleware.cors import CORSMiddleware


# ✅ 插入這段自訂 CORS middleware（建議放這裡）
def is_extension_origin(origin: str) -> bool:
    return origin.startswith("chrome-extension://")


class ExtensionCORS(CORSMiddleware):
    async def __call__(self, scope, receive, send):
        origin = None
        for header in scope.get("headers", []):
            if header[0].decode() == "origin":
                origin = header[1].decode()
                break

        if origin and is_extension_origin(origin):
            self.allow_origins = [origin]
        return await super().__call__(scope, receive, send)

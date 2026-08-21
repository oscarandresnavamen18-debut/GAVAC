from fastapi import Request, Response


class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message.get("type") == "http.response.start":
                headers = message.setdefault("headers", [])
                
                # Cabeceras de seguridad profesional (Estilo Helmet)
                security_headers = [
                    (b"X-Content-Type-Options", b"nosniff"),
                    (b"X-Frame-Options", b"DENY"),
                    (b"X-XSS-Protection", b"1; mode=block"),
                    (b"Strict-Transport-Security", b"max-age=31536000; includeSubDomains"),
                    (b"Content-Security-Policy", b"default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"),
                    (b"Referrer-Policy", b"strict-origin-when-cross-origin"),
                    (b"X-Permitted-Cross-Domain-Policies", b"none"),
                ]
                
                # Filtrar si ya existen para evitar duplicados
                existing_names = {h[0].lower() for h in headers}
                for name, value in security_headers:
                    if name.lower() not in existing_names:
                        headers.append((name, value))
                        
            await send(message)

        await self.app(scope, receive, send_wrapper)

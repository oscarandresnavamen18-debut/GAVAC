from fastapi import Request, Response


class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] == "OPTIONS":
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
<<<<<<< HEAD
                    (b"Content-Security-Policy", b"default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://images.unsplash.com https://raw.githubusercontent.com; connect-src 'self' http://127.0.0.1:8000 http://localhost:8000 http://127.0.0.1:5434 http://localhost:5434;"),
=======
                    (b"Content-Security-Policy", b"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://images.unsplash.com https://www.transparenttextures.com; connect-src 'self';"),
>>>>>>> a583192508a8de8f5f8a80617669f41a01d080f0
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

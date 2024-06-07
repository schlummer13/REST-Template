#sub imports

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
import secrets, base64, json, jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import datetime, timedelta
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

#local imports
from .database import *
from .classes import settings

# Passwort-Hashing Kontext einrichten
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#RateLimiter erstellen
limiter = Limiter(key_func=get_remote_address)

class MonitoringMiddleware(BaseHTTPMiddleware):
    """Dies die Monitoring Klasse die Daten speichert für spätere Liveauswertungen.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        if response.status_code in [400, 350, 404]:
            # Vollständige Details speichern
            request_headers = json.dumps(dict(request.headers))
            response_headers = json.dumps(dict(response.headers))

            log = APILog(
                ip=request.client.host, # type: ignore
                endpoint=request.url.path,
                method=request.method,
                request_time=start_time,
                response_time=end_time,
                duration=duration,
                status_code=response.status_code,
                request_headers=request_headers,
                response_headers=response_headers,
            )
        else:
            # Nur Basisdaten speichern
            log = APILog(
                ip=request.client.host, #type: ignore
                endpoint=request.url.path,
                request_time=start_time,
                response_time=end_time,
                duration=duration,
                status_code=response.status_code
            )
        with database.atomic():
            log.create()
        return response

def generate_secure_token(bytes:int=32):
    # Erstelle einen sicheren zufälligen Token
    random_bytes = secrets.token_bytes(bytes)  # 32 Bytes für starke Sicherheit
    # Kodiere die Bytes in base64, um sie als String darzustellen
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return token

def hash_password(password: str):
    return pwd_context.hash(password)

def create_token(custom_number:int):
    expiration_time = (datetime.now() + timedelta(hours=settings.token_valid)).timestamp()  # 24 Stunden Ablaufzeit
    token = jwt.encode(
        {"exp": expiration_time, "custom_number": custom_number},  # Token-Daten
        settings.secret,  # Geheimer Schlüssel zur Signierung des Tokens
        algorithm="HS256"
    )
    return token

def authenticate_user(mail: str, password: str):
    try:
        user: User = User.get(User.mail == mail)
        if not pwd_context.verify(password, user.password): # type: ignore
            raise HTTPException(400, "No Details")
        if not user.verified:
            raise HTTPException(350, "Not verified")
        token = create_token(user.id) # type: ignore
        return {"token": token}
    except DoesNotExist:
        raise HTTPException(400, "No Details")

def check_token(token:str):
    try:
        user: User = User.get(User.token == token)
        if user.token_date + timedelta(hours=settings.token_valid) >= datetime.now():
            user.token = None # type: ignore
            user.token_date = None # type: ignore
            user.save()
            raise HTTPException(400, "logout")
        else:
            return user
    except DoesNotExist:
       raise HTTPException(400, "Not exists")

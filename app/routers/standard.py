#submodule
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.background import BackgroundTasks
from fastapi.responses import Response, RedirectResponse
from datetime import datetime, timedelta

#internal import
from ..mailer import send_forget_password_mail, send_register, send_welcome
from ..database import Contact, User
from ..classes import ContactModel, RegisterModel, LoginModel, ForgetPasswordModel, NewPasswordModel
from ..dependencies import *


app = APIRouter()
security = HTTPBearer()

@app.post("/contact")
@limiter.limit("1/5 seconds")
async def contact(request: Request, item: ContactModel):
    """
    Use this Endpoint for your Contactform. The Message will save to a Database
    """
    data = item.model_dump()
    with db.atomic():
        Contact.create(**data)
    return Response({"message": "Success"}, 200)

@app.post("/registration", responses={400:{}})
@limiter.limit("1/5 seconds")
async def registration(request: Request, item: RegisterModel, tasks:BackgroundTasks):
    """
    This is a normal registration Endpoint.
    """
    try: 
        data = {
            "firstname": item.firstname,
            "lastname": item.lastname,
            "birth": item.birth,
            "mail": item.mail,
            "place": item.place,
            "password": hash_password(item.password),
            "verify_token": generate_secure_token(128),
            "verify_token_valid": datetime.now()
        }
        User.create(**data)
        tasks.add_task(send_register, item.mail, settings.url+f"/verfiy/{data['verify_token']}", item.firstname)
        return Response({"message": "Success"}, 200) #RedirectResponse("")
    except IntegrityError:
        raise HTTPException(400, "Mail already exists")

@app.get("/login", responses={400:{}})
@limiter.limit("1/5 seconds")
async def login(request: Request, item: LoginModel):
    """
    This is a normal Login Endpoint.
    """
    return authenticate_user(item.mail, item.password)

@app.delete("/logout", responses={400:{}})
@limiter.limit("1/5 seconds")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    This is a normal Logout Endpoint
    """
    if credentials:
        token = credentials.credentials
        user = check_token(token)
        user.token = None # type: ignore
        user.token_date = None  # type: ignore
        user.save() # type: ignore
        return Response({"message": "Success"}, 200) #RedirectResponse("")
    else:
        raise HTTPException(400, "No Token")

app.get("/verify/{token}", responses={400:{}})
@limiter.limit("1/5 seconds")
async def verify(request: Request, token:str):
    """
    This Endpoint would be called with the URL from the Verifymail.
    """
    try:
        user: User = User.get(User.verify_token == token)
        if user.verify_token_date + timedelta(days=settings.verify_valid) > datetime.now():
            User.delete_by_id(user.id)
            raise HTTPException(350, "token expired, user deleted")
        user.verify = True # type: ignore
        user.verify_token = None # type: ignore
        user.verify_token_date = None # type: ignore
        user.save()
        return Response({"message": "Success"}, 200)
    except DoesNotExist:
        raise HTTPException(400, "User already verified or unknown")

@app.post("/forget-password", responses={400:{}, 350:{}})
@limiter.limit("1/5 seconds")
async def forget_password(request: Request, item: ForgetPasswordModel, tasks: BackgroundTasks):
    """
    This Endpoints sends a Mail to the User to reset the password
    """
    try:
        user: User = User.get(User.mail == item.mail)
        if user.verified == True:
            user.verify_token = generate_secure_token()  # type: ignore
            user.verify_token_date = datetime.now() # type: ignore
            user.save()
            tasks.add_task(send_forget_password_mail, user.mail, settings.url+f"/password/{user.verify_token}", user.firstname)
            return Response({"message": "Success"}, 200)
        else:
            raise HTTPException(350, "User not verified")
    except DoesNotExist:
        raise HTTPException(400, "Unkown User")

@app.post("/new-password/{token}", responses={400:{}})
@limiter.limit("1/5 seconds")
async def new_password(request: Request, token: str, item: NewPasswordModel):
    """
    This Endpoint is to set the new Password.
    """
    try:
        user: User = User.get(User.verify_token == token)
        if user.verify_token_date + timedelta(hours=settings.token_valid) >= datetime.now():
            user.verify_token = None # type: ignore
            user.verify_token_date = None # type: ignore
            user.save()
            raise HTTPException(400, "token expired")
        else:
            user.verify_token = None # type: ignore
            user.verify_token_date = None # type: ignore
            user.password = hash_password(item.password) # type: ignore
            user.save()
            return Response({"message": "Success"}, 200)
    except DoesNotExist:
        raise HTTPException(400, "token expired")

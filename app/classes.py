from pydantic import BaseModel, EmailStr, Field
from dataclasses import dataclass
from configparser import ConfigParser

class ContactModel(BaseModel):
    mail: EmailStr = Field(
        default=...,
        example="john.doe@example.com", #type: ignore
        description="Mail from the User"
    )
    name: str = Field(
        default=...,
        example="John Doe", #type: ignore
        description="Name from the User"
    )
    text: str = Field(
        default=...,
        example="Hi! Have your more Cookies?", # type: ignore
        description="The Message from the User"
    )

class RegisterModel(BaseModel):
    firstname: str = Field(
        default=...,
        example="John", #type: ignore
        description="Firstname"
    )
    lastname: str = Field(
        default=...,
        example="Doe", #type: ignore
        description="Lastname"
    )
    place: str = Field(
        default=...,
        example="Düsseldorf", #type: ignore
        description="User's place of residence"
    )
    birth: str = Field(
        default=...,
        example="13.10.1996", #type: ignore
        description="User's date of birth in the format DD.MM.YYYY."
    )
    mail: EmailStr = Field(
        default=...,
        example="john.doe@example.com", #type: ignore
        description="User's email address."
    )
    password: str = Field(
        default=...,
        example="secret123", #type: ignore
        description="User's password. Should be secure and hard to guess."
    )

class LoginModel(BaseModel):
    mail: EmailStr = Field(
        default=...,
        example="john.doe@example.com", #type: ignore
        description="Email address the user registered with."
    )
    password: str = Field(
        default=...,
        example="secret123", #type: ignore
        description="User's password for authentication."
    )

class ForgetPasswordModel(BaseModel):
    mail: EmailStr = Field(
        default=...,
        example="john.doe@example.com", #type: ignore
        description="Email address for which a password reset is requested."
    )

class NewPasswordModel(BaseModel):
    password: str = Field(
        default=...,
        example="secret123", #type: ignore
        description="The new password the user wants to use. It should be secure and hard to guess."
    )

@dataclass
class Settings():
    url: str
    verify_valid: int
    token_valid: int
    
    secret: str
    
    host: str
    username: str
    password: str
    
    def __init__(self):
        self.read()
    
    def read(self):
        config = ConfigParser()
        config.read("app/config.ini")

        self.url = config["SETTINGS"]["URL"]
        self.verify_valid = int(config["SETTINGS"]["VERIFY_VALID"])
        self.token_valid = int(config["SETTINGS"]["TOKEN_VALID"])
        
        self.secret = config["SETTINGS"]["SECRET"]
        
        self.host = config["MAIL"]["HOST"]
        self.username = config["MAIL"]["USERNAME"]
        self.password = config["MAIL"]["PASSWORD"]

settings = Settings()
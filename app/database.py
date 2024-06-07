from peewee import * # type: ignore
from datetime import datetime

database = SqliteDatabase("app/database/logs.db")

class APILog(Model):
    id = IntegerField(primary_key=True)
    ip = CharField()
    endpoint = TextField()
    method = CharField(null=True)
    request_time = DateTimeField()
    response_time = DateTimeField()
    duration = FloatField()
    status_code = IntegerField()
    request_headers = TextField(null=True)  # Optional
    response_headers = TextField(null=True)  # Optional

    class Meta:
        database = database

db = SqliteDatabase("app/database/database.db")

class Contact(Model):
    id = AutoField(primary_key=True)
    
    name = CharField(null=False)
    mail = CharField(null=False)
    text = TextField(null=False)
    day = DateTimeField(default=datetime.now)
    
    checked = BooleanField(default=False)
    
    class Meta:
        database = db
        table_name = "Contact"

class User(Model):
    id = AutoField(primary_key=True)
    
    firstname = CharField(null=False)
    lastname = CharField(null=False)
    birth = DateField(null=False)
    place = CharField(null=False)
    

    mail = CharField(null=False, unique=True)
    password = CharField(null=False)
    token = CharField(null=True)
    token_date = DateTimeField(null=True)
    register_day = DateTimeField(default=datetime.now)
    
    verified = BooleanField(default=False)
    verify_token = CharField(null=True)
    verify_token_date = DateTimeField(null=True)
    
    def into_profil_dict(self) -> dict:
        return {"firstname": self.firstname, "lastname": self.lastname, "birth": self.birth, "place": self.place,  "mail": self.mail}
    
    class Meta:
        database = db
        table_name = "User"



with db.atomic():
    db.create_tables([Contact, User])
with database.atomic():
    APILog.create_table(True)


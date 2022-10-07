from enum import Enum
from typing import Optional, List
from fastapi import (
    FastAPI,
    Body,
    Path,
    Query,
    status,
    Form,
    Header,
    Cookie,
    File,
    UploadFile,
    HTTPException,
)
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()


class Developer(Enum):
    Frontend = "Frontend"
    Backend = "Backend"
    Fullstack = "Fullstack"


class Person(BaseModel):
    first_name: str = Field(min_length=2, max_length=15, example="Daniel")
    last_name: str = Field(min_length=2, max_length=15, example="Vilca")
    age: int = Field(gt=17, example=18)
    developer_tipe: Developer


class Person_out(Person):
    password: str = Field(example="12345678")


class Login(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    message: str = Field(default="Create Successfully")


@app.get("/")
def Welcome():
    return "Welcome to the DaniApi :D, go to documentation"


@app.get("/users")
def get_user(
    name: Optional[str] = Query(
        default=None, min_length=2, max_length=10, example="Daniel"
    ),
    age: int = Query(gt=17, example=18),
):
    return {"name": name, "age": age}


persons = [1, 2, 3, 4, 5]


@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(gt=0, example=12, description="Obtener persona segun su ID")
):
    if user_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This person doesnot exist"
        )
    return {"user": user_id, "exists": True}


@app.post("/users/create", response_model=Person, status_code=status.HTTP_201_CREATED)
def create_user(person: Person_out = Body()):
    """Create User

    Args:
        person (Person_out, optional): Crea una nueva persona. Defaults to Body().

    Returns:
        Person_out: Modelo base
    """
    return person


@app.put("/users/{user_id}", response_model=Person)
def edit_user(user_id: int = Path(gt=0, example=12), person: Person_out = Body()):
    return person


@app.post("/login", response_model=Login)
def login(username: str = Form(), password: str = Form()):
    return Login(username=username)


# Trabajando con header y cookies
@app.post("/contact", status_code=status.HTTP_201_CREATED)
def contact(
    first_name: str = Form(min_length=1, max_length=20),
    last_name: str = Form(min_length=1, max_length=20),
    email: EmailStr = Form(),
    message: str = Form(min_length=1, max_length=30),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent


# Trabajando con files
@app.post("/post-image")
def post_image(
    image: UploadFile = File(),
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, 2),
    }

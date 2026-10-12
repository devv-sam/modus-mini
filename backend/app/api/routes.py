from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class GreetRequest(BaseModel):  # defining request shape, JSON must look like this
    name: str
    excited: bool = False  # optional because has default


@router.get("/greet")
def greet(name: str) -> dict[str, str]:
    return {"message": f"hi {name}"}


@router.post("/greet")
def greet_post(req: GreetRequest) -> dict[str, str]:
    if req.excited:
        return {"message": f"hi {req.name}!"}
    else:
        return {"message": f"hi {req.name}"}

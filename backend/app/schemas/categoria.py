from pydantic import BaseModel


class CategoriaCreate(BaseModel):
    nombre: str


class CategoriaResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True
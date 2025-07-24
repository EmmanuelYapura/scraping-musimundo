from pydantic import BaseModel

class ProductoSchema(BaseModel):
    name: str
    description: str
    cashPrice: float
    price: float
    onlyDelivery: bool
    brandInfo: str
    url: str
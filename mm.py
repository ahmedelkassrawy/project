from pydantic import BaseModel, Field,EmailStr, field_validator
from fastapi import FastAPI

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls,value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        return value

app = FastAPI()

@app.post("/users")
async def create_user(user: UserCreate):
    return {
        "name": user.username,
        "message": "User created successfully"
    }

@app.get("/generate/text")
def serve_llm_controller(prompt: str) -> str:
    pipe = load_llm()
    output = generate_text(pipe,prompt)
    return {"output": output}

from typing import Literal , TypeAlias
from loguru import logger

SupportedModels: TypeAlias = Literal["gpt-3.5","gpt-4"]
PriceTable: TypeAlias = dict[SupportedModels, float]
price_table: PriceTable = {"gpt-3.5": 0.0030, 
                           "gpt-4": 0.0200}

def calc_usage_costs(
        prompt:str,response:str = None,
        model: SupportedModels,
) -> tuple[float,float,float]:
    if model not in price_table:
        raise ValueError(f"Cost calculation is not supported for {model} model.")

    price = price_table[model]


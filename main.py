from typing import Optional, List

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

# Отключаем встроенную генерацию документации по умолчанию
app = FastAPI(docs_url=None)

# 1. Эндпоинт, который отдает сам интерфейс Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="docs/swagger.yaml",
        title="Custom Swagger UI"
    )

@app.get("/docs/swagger.yaml", include_in_schema=False)
async def get_swagger_yaml():
    return FileResponse("docs/swagger.yaml")


class UserResponse(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пользователя")
    username: str
    email: str
    full_name: Optional[str] = None


# --- Имитация базы данных ---

fake_users_db = [
    {"id": 1, "username": "johndoe", "email": "john@example.com", "full_name": "John Doe"},
    {"id": 2, "username": "janedoe", "email": "jane@example.com", "full_name": "Jane Doe"}
]


# --- Эндпоинты (Контроллеры) ---

@app.get("/users", response_model=List[UserResponse], tags=["Users"])
async def get_users():
    """
    Получить список всех пользователей.

    Возвращает полный список зарегистрированных пользователей из базы данных.
    """
    return fake_users_db
from fastapi import FastAPI
from routers import car_router, user_router, rental_router, review_router
from fastapi.openapi.utils import get_openapi


app = FastAPI()


def custom_openapi():
  if app.openapi_schema:
    return app.openapi_schema

  openapi_schema = get_openapi(
      title="Вариант 7: Аренда автомобилей",
      version="0.1",
      routes=app.routes,
  )

  openapi_schema.setdefault("components", {})
  openapi_schema["components"]["securitySchemes"] = {
      "BearerAuth": {
          "type": "http",
          "scheme": "bearer",
          "bearerFormat": "JWT",
      }
  }

  app.openapi_schema = openapi_schema
  return openapi_schema


app.openapi = custom_openapi


@app.get(
  path="/",
  summary="Информация об API",
  tags=["Общий доступ"],
)
def info_about_api():
  return {"info": "Задание на экзамен по дисциплине «Разработка серверной части веб-приложений». Вариант 7: Система аренды автомобилей (Веб API). Выполнил Гологузов Егор, Т-323901-ИСТ."}


app.include_router(car_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(rental_router, prefix="/api")
app.include_router(review_router, prefix="/api")

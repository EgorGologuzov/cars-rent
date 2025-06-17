from fastapi import FastAPI
from routers import car_router


app = FastAPI()


@app.get(
  path="/",
  summary="Информация об API",
  tags=["Информация"]
)
def info_about_api():
  return {"info": "Задание на экзамен по дисциплине «Разработка серверной части веб-приложений». Вариант 7: Система аренды автомобилей (Веб API). Выполнил Гологузов Егор, Т-323901-ИСТ."}


app.include_router(car_router, prefix="/api")

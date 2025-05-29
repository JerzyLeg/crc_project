from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from logic import (
    isInt, isLeapYear, isMonthValid, isDayValid,
    findDoomsday, finalDay
)

app = FastAPI()

dayList = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

class DateInput(BaseModel):
    day: int
    month: int
    year: int

    
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("index.html", "r") as file:
        return file.read()

@app.post("/doomsday")
def get_day_of_week(date: DateInput):
    if not isMonthValid(date.month) or not isDayValid(date.day, date.month, isLeapYear(date.year)):
        return {"error": "Invalid date"}

    doomsday = findDoomsday(date.year)
    weekday = finalDay(date.month, date.day, doomsday, isLeapYear(date.year))
    return {
        "date": f"{date.day}.{date.month}.{date.year}",
        "day": dayList[weekday]
    }
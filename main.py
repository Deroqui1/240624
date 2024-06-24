from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Event(BaseModel):
    id: int
    title: str
    date: str
    description: str

events: List[Event] = []

@app.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    return templates.TemplateResponse("list_events.html", {"request": request, "events": events})

@app.get("/events/create", response_class=HTMLResponse)
async def create_event_form(request: Request):
    return templates.TemplateResponse("create_event.html", {"request": request})

@app.post("/events/create")
async def create_event(title: str = Form(...), date: str = Form(...), description: str = Form(...)):
    event_id = len(events) + 1
    new_event = Event(id=event_id, title=title, date=date, description=description)
    events.append(new_event)
    return RedirectResponse("/events", status_code=302)

@app.get("/events/edit/{event_id}", response_class=HTMLResponse)
async def edit_event_form(request: Request, event_id: int):
    event = next((event for event in events if event.id == event_id), None)
    return templates.TemplateResponse("edit_event.html", {"request": request, "event": event})

@app.post("/events/edit/{event_id}")
async def edit_event(event_id: int, title: str = Form(...), date: str = Form(...), description: str = Form(...)):
    event = next((event for event in events if event.id == event_id), None)
    if event:
        event.title = title
        event.date = date
        event.description = description
    return RedirectResponse("/events", status_code=302)

@app.get("/events/delete/{event_id}")
async def delete_event(event_id: int):
    global events
    events = [event for event in events if event.id != event_id]
    return RedirectResponse("/events", status_code=302)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

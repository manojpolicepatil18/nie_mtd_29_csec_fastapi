from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app=FastAPI()
@app.get("/")
def home():
        return {"message": "enterprise IT service desk"}
db = {
    1 : {"id":1, "title":"refund issue",
         "description":"issue is in progress",
         "category":"software","status":"NEW"},
    2 : {"id":2, "title":"recived damaged product",
         "description":"handling problem",
         "category":"Hardware","status":"NEW"}
}

class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str
    
class TicketResponse(TicketCreate):
    id: int

@app.get("/tickets")
def ticket_read_all():
    return list(db.values())

@app.get("/tickets/{id}")
def ticket_read_by_id(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db[id]

@app.post("/tickets",status_code=201,response_model=TicketResponse)
def ticket_create(ticket_payload: TicketCreate):
    new_id = max(db.keys()) + 1 if db else 1
    ticket = {"id": new_id, **ticket_payload.model_dump()}
    db[new_id] = ticket
    return ticket

@app.put("/tickets/{id}",response_model=TicketResponse)
def ticket_update(id: int, ticket_payload: TicketCreate):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket = {"id": id, **ticket_payload.model_dump()}
    db[id] = ticket
    return ticket

@app.delete("/tickets/{id}")
def ticket_delete(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    del db[id]
    return {"message": "Ticket deleted successfully"}
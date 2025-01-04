from fastapi import FastAPI
import logging
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
app = FastAPI()


@app.get("/")
def book_ticket():
    # TODO : 
    return {'message': 'Hello, FastAPIIII'}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

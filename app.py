from fastapi import FastAPI
from chains.book_chain import inference,inference_stream
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
app=FastAPI()


class Query(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Welcome to Stanford CS229 notes RAG based chatbot made by Prabhsimrat Singh"}




@app.post("/predict")
def get_summary(data:Query):
    result=inference(data.text)
    return result


@app.post("/stream")
def predict(data: Query):

    return StreamingResponse(
        inference_stream(data.text),
        media_type="text/plain"
    )
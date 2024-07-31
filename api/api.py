from fastapi import FastAPI


app = FastAPI()


@app.post("/hello")
async def hello():
    return "hello"

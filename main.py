from fastapi import FastAPI

from database import Base, engine
from endpoints import router, task_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.include_router(task_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

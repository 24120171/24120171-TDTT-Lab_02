from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers.auth import router as auth_router
from backend.app.routers.todo import router as todo_router 

app = FastAPI(title="Todo App Backend") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(todo_router)

@app.get("/")
def root():
    return {"message": "Welcome to Todo App API"}

@app.get("/health")
def health():
    return {"status": "ok"}
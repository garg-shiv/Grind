from fastapi import FastAPI

app = FastAPI()

# Basic route
@app.get("/")
def home():
    return {"message": "Server is running"}


# GET with query parameters
@app.get("/greet")
def greet_user(name: str, age: int = None):
    return {
        "message": f"Hello {name}",
        "age": age
    }


# POST example
@app.post("/create-user")
def create_user(user: dict):
    return {
        "message": "User created",
        "user": user
    }

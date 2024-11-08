from fastapi import FastAPI
import sqlite3


app = FastAPI()


# Now define your API routes
@app.get("/api/py/helloFastApi")
async def read_root():
    return {"message": "Hello, FastAPI with populated data!"}

# Your other routes can now access the populated data

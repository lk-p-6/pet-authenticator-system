from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
import asyncio
import secrets
import time

current_code = {
    "value": f"{secrets.randbelow(1_000_000):06d}",
    "code_generated_at": time.perf_counter()
}
ttl = 10.0

async def number_generator():
    global current_code
    while True:
        current_code = {
            "value": f"{secrets.randbelow(1_000_000):06d}",
            "code_generated_at": time.perf_counter()
        }
        print("Generated:", current_code["value"])
        await asyncio.sleep(ttl)

def verifyCalc(user_code, now, current_code, ttl):
    return user_code == current_code["value"] and (now - current_code["code_generated_at"]) <= ttl

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: launching generator")
    task = asyncio.create_task(number_generator())
    yield
    print("Shutdown: stopping generator")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

class Verify(BaseModel):
    code: str = Field(pattern=r"^\d{6}$")

app = FastAPI(lifespan=lifespan)
@app.post("/verify")
def check_code(verify: Verify):
    now = time.perf_counter()
    code_snapshot = current_code.copy()
    return{"isCorrect": verifyCalc(verify.code, now, code_snapshot, ttl)}

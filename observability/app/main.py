from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
import logging, random,time
from prometheus_client import (
    Counter,Histogram,generate_latest,CONTENT_TYPE_LATEST,CollectorRegistry,multiprocess
)

from prometheus_fastapi_instrumentator import Instrumentator
from typing import List,Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger=logging.getLogger(__name__)

REQUEST=Counter(
    "fastapi_request_total",
    "Total count of requests by method and path",
    ["method","path","status"]
)

LATENCY=Histogram(
    "fastapi_requests_latency_status",
    "Request latency by method and path",
    ["method","path"]
)

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Startup
    logger.info("Starting up FASTAPI application.")
    yield
    #Shutdown
    logger.info("Shutting down FastAPI application.")


app=FastAPI(lifespan=lifespan)

### initialize prometheus instrumentation
Instrumentator().instrument(app).expose(app)


#Example data store
todos: List[Dict]=[]

@app.get("/")
async def read_root():
    REQUEST.labels(method="GET", path="/",status=200).inc()
    logger.info("Root end point accessed.")
    return {"status":"healthy"}

@app.get("/todos")
async def get_todos():
    start_time=time.time()
    logger.info("Fetching all todos")

    # simulate random latency

    time.sleep(random.uniform(0.1,0.5))

    REQUEST.labels(method="GET",path="/todos",status=200).inc()
    LATENCY.labels(method="GET",path="/todos").observe(time.time()-start_time)


@app.post("/todos")
async def create_todo(title: str):
    start_time=time.time()
    logger.info(f"creating new todo: {title}")

    if not title:
        REQUEST.labels(method="POST",path="/todos",status=400).inc()
        raise HTTPException(status_code=400,detail="Title cannot be empty")
        todo={"id": len(todos)+1,"title":title,"completed":False}
        todos.append(todo)
        REQUEST.labels(method="POST",path="/todos",status=400).inc()
        LATENCY.labels(method="POST",path="/todos").observe(time.time()-start_time)
        return todo


@app.get("/metrics")
async def metrics():
    return generate_latest()


@app.get("/error")
async def trigger_error():
    logger.error("simulated error endpoint accessed")
    raise HTTPException(status_code=500,detail="Simulated error")
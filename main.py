from fastapi import FastAPI, Query, HTTPException
import httpx
from datetime import datetime

app = FastAPI()
@app.get("/departures")
def get_dep(q:str = Query(...)):
    if len(q) < 3:
      raise HTTPException(
        status_code=400,
        detail = "Query must be at least 3 characters long"
      )
    return {"message": "working", "query": q}






#Step 2 : Call iRail to fetch matching stations
#Step 3 : For each station, fetch departures and filter to 15 minutes

from fastapi import FastAPI, Header
from typing import Optional
import uuid
app = FastAPI()

@app.get("/getRequest")
def readHeaders(qParam: str | None = None,
                txId: int = Header(),
                authKey: str = Header(),
                optionalKey: Optional[str] = Header(default=None)):
    return { 
        "Status" : "This is Get Operation",
        "empId": txId,
        "authKey" : authKey,
        "optionalKey": optionalKey,
        "qParam" : qParam,
        "uuId4" : uuid.uuid4()
        }
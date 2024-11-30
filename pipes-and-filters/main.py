from fastapi import FastAPI, HTTPException
from filters.filter import FilterFilter
from filters.publish import PublishFilter
from filters.scream import ScreamingFilter
from message import Message
from pipe import Pipe
from pydantic import BaseModel, Field

STOP_WORDS = {"bird-watching", "ailurophobia", "mango"}

app = FastAPI()

inp_pipe, filter_pipe, scream_pipe = Pipe(), Pipe(), Pipe()
flt_filter = FilterFilter([inp_pipe], [filter_pipe], STOP_WORDS)
scream_filter = ScreamingFilter([filter_pipe], [scream_pipe])
publish_filter = PublishFilter([scream_pipe], [])

flt_filter.run()
scream_filter.run()
publish_filter.run()

class ReqMessage(BaseModel):
    from_: str = Field(..., alias="from", min_length=1)
    message: str = Field(..., min_length=1)

@app.post("/messages")
def post_message(req_message: ReqMessage):
    try:
        data = req_message.dict(by_alias=True)

        message =  Message(data["from"], data["message"])
        inp_pipe.send(message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
    


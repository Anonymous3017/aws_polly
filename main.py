import uvicorn
from fastapi import FastAPI
from functools import lru_cache
from pydantic import BaseModel
import boto3
from fastapi.responses import StreamingResponse
import base64
import io
import config


app = FastAPI()
 
@lru_cache()
def get_settings():
    return config.Settings()
 
class Text(BaseModel):
    content: str
    output_format: str
 
 
@app.post("/")
async def get_audio(text: Text):
    client = boto3.client("polly", aws_access_key_id = get_settings().AWS_AK, aws_secret_access_key = get_settings().AWS_SAK, region_name = "us-east-1")
    result = client.synthesize_speech(Text = text.content, OutputFormat = text.output_format, VoiceId = "Joanna")
    audio=result["AudioStream"].read()
    with open("audio.mp3","wb") as file:
        file.write(audio)

 
 
    return {"message":text.content}
 
#run app
if __name__ == "__main__":
    uvicorn.run("main:app",host = "0.0.0.0", port = 8000, reload =True)
 
 
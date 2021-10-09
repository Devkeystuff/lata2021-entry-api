import argparse
from fastapi import FastAPI, UploadFile, File, Query

from starlette.responses import Response°

from models.messages.message_request_generate_design import MessageRequestGenerateDesign
from models.messages.message_response_generate_design import MessageResposneGenerateDesign

from controllers.controller_requests import ControllerRequests
from typing import List

from modules.logging_utils import LoggingUtils

app = FastAPI()
parser = argparse.ArgumentParser()
parser.add_argument('-debug', default=True)

@app.post('/generate_design', response_model=MessageResponseGenerateDesign)
def generate_design(api_key: str, title: str, desc: str, qr_image: UploadFile, world_image: UploadFile):
  response = None


if __name__ == '__main__':
  LoggingUtils.init(prefix='api')
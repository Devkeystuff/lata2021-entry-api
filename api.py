import argparse
from logging import debug
from dataclasses_json.cfg import T
import uvicorn
from fastapi import FastAPI, UploadFile, File, Query

from starlette.responses import Response

from models.messages.message_request_generate_design import MessageRequestGenerateDesign
from models.messages.message_response_generate_design import MessageResponseGenerateDesign

from controllers.controller_requests import ControllerRequests
from typing import List

from modules.logging_utils import LoggingUtils

app = FastAPI()
parser = argparse.ArgumentParser()
parser.add_argument('-debug', default=True, type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-workers', default=1, type=int)
args, _ = parser.parse_known_args()

@app.post('/generate_design', response_model=MessageResponseGenerateDesign)
def generate_design(
  api_key: str = Query(...), 
  title: str = Query(...), 
  desc: str = Query(...), 
  qr_image: UploadFile = File(...), 
  world_image: UploadFile = File(...)
):
  response = None
  try:
    message_request_generate_design = MessageRequestGenerateDesign()
    message_request_generate_design.api_key = api_key
    message_request_generate_design.title = title
    message_request_generate_design.desc = desc
    message_request_generate_design.qr_img_file_name = qr_image.filename
    message_request_generate_design.world_img_file_name = world_image.filename

    response = ControllerRequests.generate_design(
      request=message_request_generate_design, 
      qr_image=qr_image, 
      world_image=world_image
    )

  except Exception as e:
    LoggingUtils.log_exception(e)
  return Response(content=response.to_json(), media_type='application/json')


if __name__ == '__main__':
  uvicorn.run(
    'api:app',
    debug=args.debug,
    reload=args.debug,
    workers=args.workers
  )
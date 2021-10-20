import argparse
import uvicorn
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import Response
from models.messages.message_request_elevation_map import MessageRequestElevationMap

from models.messages.message_request_generate_design import MessageRequestGenerateDesign
from models.messages.message_response_elevation_map import MessageResponseElevationMap
from models.messages.message_response_generate_design import MessageResponseGenerateDesign

from controllers.controller_requests import ControllerRequests

from modules.logging_utils import LoggingUtils

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
parser = argparse.ArgumentParser()
parser.add_argument('-debug', default=True, type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-workers', default=1, type=int)
args, _ = parser.parse_known_args()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/generate_design', response_model=MessageResponseGenerateDesign)
async def generate_design(
        api_key: str = Query(...),
        title: str = Query(...),
        description: str = Query(...),
        qr_image: UploadFile = File(...),
        world_image: UploadFile = File(...)
):
    response = None
    try:
        message_request_generate_design = MessageRequestGenerateDesign()
        message_request_generate_design.api_key = api_key
        message_request_generate_design.title = title
        message_request_generate_design.description = description
        message_request_generate_design.qr_img_file_name = qr_image.filename
        message_request_generate_design.world_img_file_name = world_image.filename

        response = await ControllerRequests.generate_design(
            request=message_request_generate_design,
            qr_image=qr_image,
            world_image=world_image
        )

    except Exception as e:
        LoggingUtils.log_exception(e)
    return Response(content=response.to_json(), media_type='application/json')

@app.post('/get_elevation_map', response_model=MessageResponseElevationMap)
async def get_elevation_map(
  api_key: str = Query(...),
  south: float = Query(...),
  north: float = Query(...),
  west: float = Query(...),
  east: float = Query(...),
):
  response = None
  try:
    message_request_get_elevation_map = MessageRequestElevationMap()
    message_request_get_elevation_map.api_key = api_key
    message_request_get_elevation_map.south = south
    message_request_get_elevation_map.north = north
    message_request_get_elevation_map.west = west
    message_request_get_elevation_map.east = east

    response = await ControllerRequests.get_elevation_map(request=message_request_get_elevation_map)
  except Exception as e:
    LoggingUtils.log_exception(e)
  return Response(content=response.to_json(), media_type='multipart/form-data')


if __name__ == '__main__':
    uvicorn.run(
        'api:app',
        debug=args.debug,
        reload=args.debug,
        workers=args.workers
    )


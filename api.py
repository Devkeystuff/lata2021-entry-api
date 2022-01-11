import argparse
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import Response

from models.messages.message_request_generate_design import MessageRequestGenerateDesign
from models.messages.message_response_generate_design import MessageResponseGenerateDesign
from models.messages.message_request_get_design import MessageRequestGetDesign
from models.messages.message_response_get_design import MessageResponseGetDesign

from controllers.controller_requests import ControllerRequests

from modules.logging_utils import LoggingUtils

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
parser = argparse.ArgumentParser()
parser.add_argument('-debug', default=True,
                    type=lambda x: (str(x).lower() == 'true'))
parser.add_argument('-workers', default=1, type=int)
args, _ = parser.parse_known_args()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://humboldtapparel.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/generate_design', response_model=MessageResponseGenerateDesign)
async def generate_design(
    api_key: str = Query(...),
    is_preview: bool = Query(...),
    title: str = Query(...),
    description: str = Query(...),
    west: float = Query(...),
    north: float = Query(...),
    east: float = Query(...),
    south: float = Query(...),
):
    response = None
    try:
        message_request_generate_design = MessageRequestGenerateDesign()
        message_request_generate_design.api_key = api_key
        message_request_generate_design.is_preview = is_preview
        message_request_generate_design.title = title
        message_request_generate_design.description = description
        message_request_generate_design.west = west
        message_request_generate_design.north = north
        message_request_generate_design.east = east
        message_request_generate_design.south = south

        response = await ControllerRequests.generate_design(
            request=message_request_generate_design,
        )

    except Exception as e:
        LoggingUtils.log_exception(e)
    return Response(content=response.to_json(), media_type='application/json')


@app.post('/get_design', response_model=MessageResponseGetDesign)
async def get_design(
    api_key: str = Query(...),
    design_uuid: str = Query(...)
):
    response = None
    try:
        message_request_get_design = MessageRequestGetDesign()
        message_request_get_design.api_key = api_key
        message_request_get_design.design_uuid = design_uuid

        response = ControllerRequests.get_design(
            request=message_request_get_design)
    except Exception as e:
        LoggingUtils.log_exception(e)
    return response
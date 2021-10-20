import io
import aiofiles
import requests
import uuid
import qrcode
from PIL import Image
from fastapi import UploadFile
from models.messages.message_request_elevation_map import MessageRequestElevationMap
from models.messages.message_response_elevation_map import MessageResponseElevationMap
from modules import consts

from modules.consts import PATH_3D_WORLD

from models.enums.enum_error_code import ErrorCode
from models.enums.enum_error_message import ErrorMessage

from modules.logging_utils import LoggingUtils

from controllers.controller_database import ControllerDatabase

from models.messages.message_request_generate_design import MessageRequestGenerateDesign
from models.messages.message_response_generate_design import MessageResponseGenerateDesign


class ControllerRequests:
    @staticmethod
    async def generate_design(
            request: MessageRequestGenerateDesign,
            qr_image: UploadFile,
            world_image: UploadFile
    ) -> MessageResponseGenerateDesign:
        response = None
        try:
            response = MessageResponseGenerateDesign()
            if ControllerRequests.validate_request(request, response):
                if ControllerRequests.validate_image_file(qr_image, response):
                    if ControllerRequests.validate_tiff_file(world_image, response):
                        request_uuid = str(uuid.uuid4())
                        request.design_uuid = request_uuid

                        ControllerDatabase.insert_design(design=request)

                        qr_code_img = qrcode.make(f'{PATH_3D_WORLD}/{request.design_uuid}')
                        height_map_img = await ControllerRequests.get_elevation_map()

                        response.is_success = True
                        response.design_uuid = request_uuid
        except Exception as e:
            LoggingUtils.log_exception(e)
        return response
    
    @staticmethod
    async def get_elevation_map(
        request: MessageRequestElevationMap
    ) -> MessageResponseElevationMap:
        response = None
        try:
            response = MessageResponseElevationMap()
            if ControllerRequests.validate_request(request, response):
                url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={request.south}&north={request.north}&west={request.west}&east={request.east}'
                res = requests.get(url)
                image_source = f'{consts.PATH_QR_IMG}/test.png'
#                
                with Image.open(io.BytesIO(res.content)) as img:
                  img.save('./static/test.png', "PNG")

                # image.save(image_source, 'PNG')
        except Exception as e:
            LoggingUtils.log_exception(e)
        return response

    @staticmethod
    def validate_request(request, response) -> bool:
        status = False
        try:
            if ControllerRequests.check_api_key(request.api_key):
                status = True
            else:
                response.error_code = ErrorCode.WRONG_API_KEY.value
                response.error_desc = response.error_desc + ErrorMessage.WRONG_API_KEY.value
        except Exception as e:
            LoggingUtils.log_exception(e)
        return status

    @staticmethod
    def validate_image_file(file: UploadFile, response):
        status = False
        try:
            file_extension = file.filename.split('.')[-1]
            if file_extension == 'jpg' or 'png':
                status = True
            else:
                response.error_code = ErrorCode.WRONG_FILE_FORMAT.value
                response.error_desc = response.error_desc + ErrorMessage.WRONG_FILE_FORMAT.value
        except Exception as e:
            LoggingUtils.log_exception(e)
        return status

    @staticmethod
    def validate_tiff_file(file: UploadFile, response):
        status = False
        try:
            file_extension = file.filename.split('.')[-1]
            if file_extension == 'tif':
                status = True
            else:
                response.error_code = ErrorCode.WRONG_FILE_FORMAT.value
                response.error_desc = response.error_desc + ErrorMessage.WRONG_FILE_FORMAT.value
        except Exception as e:
            LoggingUtils.log_exception(e)
        return status

    @staticmethod
    def check_api_key(api_key: str) -> bool:
        status = False
        try:
            client = ControllerDatabase.get_client(api_key)
            if client is not None:
                status = True
        except Exception as e:
            LoggingUtils.log_exception(e)
        return status

    @staticmethod
    async def write_file(path: str, file):
        try:
            async with aiofiles.open(path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
        except Exception as e:
            LoggingUtils.log_exception(e)
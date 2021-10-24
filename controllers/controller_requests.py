import io
import os
import aiofiles
import requests
import uuid
import qrcode
from PIL import Image
from fastapi import UploadFile
from modules.generate_utils import ImageGenerator
from modules.consts import HOST, PATH_3D_WORLD, PATH_PUBLIC, PATH_STATIC, PATH_STATIC_ABSOLUTE

from models.enums.enum_error_code import ErrorCode
from models.enums.enum_error_message import ErrorMessage

from models.common.lat_lng_bounds import LatLngBounds

from modules.logging_utils import LoggingUtils

from controllers.controller_database import ControllerDatabase

from models.messages.message_request_generate_design import MessageRequestGenerateDesign
from models.messages.message_response_generate_design import MessageResponseGenerateDesign


class ControllerRequests:
    @staticmethod
    async def generate_design(
        request: MessageRequestGenerateDesign,
    ) -> MessageResponseGenerateDesign:
        response = None
        try:
            response = MessageResponseGenerateDesign()
            if ControllerRequests.validate_request(request, response):
                request_uuid = str(uuid.uuid4())
                request.design_uuid = request_uuid

                # ControllerDatabase.insert_design(design=request)

                bounds = LatLngBounds(
                    west=request.west,
                    north=request.north,
                    east=request.east,
                    south=request.south
                )
                elevation_map_img = ImageGenerator.generate_elevation_map_img(
                    bounds)
                qr_code_img = ImageGenerator.generate_qr_img(
                    f'{PATH_3D_WORLD}/{request.design_uuid}')

                distorted_map_img = ImageGenerator.generate_distorted_map(
                    h_map=elevation_map_img, img=f'{PATH_PUBLIC}/images/lines.png')
                design_img = ImageGenerator.generate_design_image(
                    location_name=request.title, side_text=request.description, map_img=distorted_map_img, qr_code_img=qr_code_img)

                save_path = f'{PATH_STATIC}/resources/{request_uuid}'

                os.mkdir(save_path)
                elevation_map_img.save(f'{save_path}/elevation.png', 'PNG')
                qr_code_img.save(f'{save_path}/qr.png', 'PNG')

                response.qr_code_img = f'{PATH_STATIC_ABSOLUTE}/resources/{request_uuid}/qr.png'
                response.elevation_map_img = f'{PATH_STATIC_ABSOLUTE}/resources/{request_uuid}/elevation.png'
                response.design_uuid = request_uuid
                response.is_success = True
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

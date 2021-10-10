import aiofiles
import uuid
from fastapi import UploadFile
from modules import consts

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
                    if ControllerRequests.validate_gltf_file(world_image, response):
                        request_uuid = str(uuid.uuid4())
                        request.design_uuid = request_uuid

                        ControllerDatabase.insert_design(design=request)

                        qr_file_extension = qr_image.filename.split('.')[-1]
                        world_file_extension = world_image.filename.split('.')[-1]
                        qr_file_source = f'{consts.PATH_QR_IMG}/{request_uuid}.{qr_file_extension}'
                        world_file_source = f'{consts.PATH_WORLD_IMG}/{request_uuid}.{world_file_extension}'

                        await ControllerRequests.write_file(qr_file_source, qr_image)
                        await ControllerRequests.write_file(world_file_source, world_image)

                        response.is_success = True
                        response.design_uuid = request_uuid
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
    def validate_gltf_file(file: UploadFile, response):
        status = False
        try:
            file_extension = file.filename.split('.')[-1]
            if file_extension == 'gltf':
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
import uuid
from fastapi import UploadFile

from modules.logging_utils import LoggingUtils

from models.messages.message_request_generate_design import MessageRequestGenerateDesign
from models.messages.message_response_generate_design import MessageResponseGenerateDesign

class ControllerRequests:

  @staticmethod
  def generate_design(request: MessageRequestGenerateDesign, qr_image: UploadFile, world_image: UploadFile):
    response = None
    try:
      response = MessageResponseGenerateDesign()
    except Exception as e:
      LoggingUtils.log_exception(e)
    pass 
import uuid
from fastapi import UploadFile

class ControllerRequests:

  @staticmethod
  def generate_design(request: MessageRequestGenerateDesign, qr_image: UploadFile, world_image: UploadFile):
    response = None
    try:
    except Exception as e:
      LoggingUtils.log_exception(e)
    pass 
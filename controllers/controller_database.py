from modules.logging_utils import LoggingUtils

from models.db.db_design import DbDesign

class ControllerDatabase:
  @staticmethod
  def insert_design(design: DbDesign):
    design_id = 0
    try:
      design_id = 1
    except Exception as e:
      LoggingUtils.log_exception(e)
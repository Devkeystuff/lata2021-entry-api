from dacite import from_dict, Config

from modules.logging_utils import LoggingUtils
from modules.db_cursor import DbCursor

from models.db.db_design import DbDesign
from models.db.db_client import DbClient

from models.messages.message_request_generate_design import MessageRequestGenerateDesign


class ControllerDatabase:
    @staticmethod
    def insert_design(design: MessageRequestGenerateDesign) -> int:
        design_id = 0
        try:
            cols = [
                'design_uuid',
                'qr_img_file_name',
                'world_img_file_name',
                'title',
                'description',
            ]
            with DbCursor() as cursor:
                cursor.execute(
                    f'INSERT INTO designs ({", ".join(cols)}) '
                    f'VALUES ({", ".join([f"%({it})s" for it in cols])}) '
                    f'RETURNING design_id',
                    design.__dict__
                )
                design_id, = cursor.fetchone()
        except Exception as e:
            LoggingUtils.log_exception(e)
        return design_id

    @staticmethod
    def get_client(api_key: str) -> DbClient:
        client = None
        try:
            with DbCursor() as cursor:
                cursor.execute(
                    f'SELECT '
                    f'client_id, '
                    f'name, '
                    f'api_key, '
                    f'is_deleted, '
                    f'created, '
                    f'modified '
                    f'FROM clients '
                    f'WHERE api_key=%(api_key)s '
                    f'AND NOT is_deleted '
                    f'LIMIT 1',
                    {
                        'api_key': api_key
                    }
                )

                row = cursor.fetchone()
                if row:
                    columns = [it[0] for it in cursor.description]
                    client_dict = dict(zip(columns, row))
                    client = from_dict(
                        data_class=DbClient,
                        data=client_dict,
                        config=Config(check_types=False)
                    )
        except Exception as e:
            LoggingUtils.log_exception(e)
        return client

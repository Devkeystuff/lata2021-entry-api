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
                'qr_code_img',
                'elevation_map_img',
                'lines_design_img',
                'title',
                'description',
                'edition_title',
                'edition_desc'
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

    @staticmethod
    def get_design_by_uuid(uuid: str) -> DbDesign:
        design = None
        try:
            with DbCursor() as cursor:
                cursor.execute(
                    f'SELECT '
                    f'design_id, '
                    f'design_uuid, '
                    f'title, '
                    f'description, '
                    f'qr_code_img, '
                    f'elevation_map_img, '
                    f'lines_design_img, '
                    f'edition_title, '
                    f'edition_desc '
                    f'FROM designs '
                    f'WHERE design_uuid=%(uuid)s '
                    f'AND NOT is_deleted '
                    f'LIMIT 1',
                    {
                        'uuid': uuid
                    }
                )
                row = cursor.fetchone()
                if row:
                    columns = [it[0] for it in cursor.description]
                    print(columns)
                    design_dict = dict(zip(columns, row))
                    design = from_dict(
                        data_class=DbDesign,
                        data=design_dict,
                        config=Config(check_types=False)
                    )
        except Exception as e:
            LoggingUtils.log_exception(e)
        return design

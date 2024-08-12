import sqlite3
from Utilities_jmorga24.log import get_logger
from Utilities_jmorga24.config import Config

log = get_logger("db")

CHECK_TABLE = "SELECT tbl_name FROM sqlite_master WHERE type='table' AND name=?"
TABLE_EXISTS = "Table exists with table name: %s"
INVALID_SQL = "Cant create a table with sql: %s"

__db = Config().db["dbname"]
__connection = None

log.info("Starting DB connection db name: %s", __db)
__connection = sqlite3.connect(__db)
__cur = __connection.cursor()


def ensure_table(table_name: str, sql: str = None) -> None:
    try:
        listOfTables = __cur.execute(CHECK_TABLE, (table_name,)).fetchall()
        log.info(TABLE_EXISTS, table_name)
    except Exception as e:
        log.error(e)

    if len(listOfTables) > 0:
        return

    if sql == None or sql.isspace():
        log.error(INVALID_SQL, sql)
        raise ValueError("sql has no value")




if __name__ == "__main__":
    try:
        print(ensure_table(table_name="dummyXX".upper()))
    except ValueError as e:
        log.error(e)

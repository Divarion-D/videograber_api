from application.libs.db_query import DataBase, QueryBuilder

QB = QueryBuilder(DataBase(), "db.db")


def add_table_bd() -> None:
    # create table video_files
    QB.reset()  # reset query builder
    QB.query(
        """CREATE TABLE IF NOT EXISTS video_files ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "kp_id" TEXT, "player" TEXT, "translation" TEXT, "player_key" TEXT)"""
    )


# Нормалиировка текста
def normalize(text):
    # trim, to lower, replace
    text = text.strip().lower().replace("ё", "е")
    return text

import sqlite3
import json


# def json_to_sqlite(sqlite_db, table_name, json_list):
#     someitem = json_list[0]
#     columns = list(someitem.keys())
#
#     query = "insert into {0} (timestamp,{1}) values (?{2})"
#     query = query.format(table_name, ",".join(columns), ",?" * len(columns))
#
#     for item in json_list:
#         c = sqlite_db.cursor()
#         c.execute(query, item.values())
#         c.close()


def json_to_sqlite(sqlite_db, table_name, json_list):
    someitem = json_list[0]
    columns = list(someitem.keys())

    # Create the table
    sqlite_db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")

    query = "INSERT INTO {0} ({1}) VALUES ({2})"
    query = query.format(table_name, ",".join(columns), ','.join("?" * len(columns)))

    for item in json_list:
        c = sqlite_db.cursor()
        c.execute(query, [
            val
            for val in item.values()

        ])
        c.close()
    
    sqlite_db.commit()
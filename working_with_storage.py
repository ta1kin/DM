import sqlite3

DATA_TABLE = [
    (1, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (2, '0000\n0000\n0000\n0000', '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (3, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (4, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (5, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (6, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (7, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (8, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (9, '0000\n0000\n0000\n0000', '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (10, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (11, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (12, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (13, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (14, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1'),
    (15, '0000\n0000\n0000\n0000',  '1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1')
]

INDEX_DATA = []

def init():
    db = sqlite3.connect('data.db')
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS matrics (
        id INT PRIMARY KEY,
        old_matrics VARCHAR(100),
        new_matrics VARCHAR(100)
    );''')

def delit(id: object) -> object:
    with sqlite3.connect('data.db') as db:
        cursor = db.cursor()
        if len(select(all=1)) > 0:
            cursor.execute(f'''DELETE FROM matrics WHERE id={id};''')

def select(id=None, all=False):
    with sqlite3.connect('data.db') as db:
        cursor = db.cursor()
    if all:
        value = cursor.execute('''SELECT * FROM matrics;''').fetchall()
        return value
    elif id is not None:
        value = cursor.execute(f'''SELECT * FROM matrics WHERE id={id};''').fetchall()
        # print(value)
        return value[0]
    else:
        value = cursor.execute(f'''SELECT * FROM matrics ORDER BY id DESC LIMIT 1;''').fetchall()
        return value[0]

def insert(value):
    with sqlite3.connect('data.db') as db:
        cursor = db.cursor()
        cursor.execute(f'''INSERT INTO matrics VALUES ({value[0]}, '{value[1]}', '{value[2]}', '{value[3]}');''')
        # print(cursor.execute('''SELECT * FROM matrics;''').fetchall()[0])


from common.database import DB

def register_user(email, password):

    if not is_registered(email):
        con = DB.connection
        cur = con.cursor()

        cur.execute('INSERT INTO lysr_user (email, password) VALUES (%s, %s)', (email, password))
        con.commit()

        return True

    return False

def check_user_credentials(email, password):

    if is_registered(email):
        con = DB.connection
        cur = con.cursor()

        cur.execute('SELECT id FROM lysr_user WHERE email = %s and password = %s', (email, password))
        con.commit()

        if cur.rowcount is 1:
            return cur.fetchone()[0]

        return None

def is_registered(email):
    con = DB.connection
    cur = con.cursor()

    cur.execute('SELECT id FROM lysr_user WHERE email = %s', (email,))
    con.commit()

    if cur.rowcount is 0:
        return False

    return True

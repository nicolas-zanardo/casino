import pymysql.cursors


def connection():
    try:
        connection = pymysql.connect(host='mysql-nicolas1981.alwaysdata.net',
                                     user='332914',
                                     password='casino_project',
                                     database='nicolas1981_casino',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except:
        print("error connection SQL")


def createPlayer(userName, gain):
    con = connection()
    with con:
        with con.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `player` (`name`, `gain`) VALUES (%s, %s)"
            cursor.execute(sql, (userName, gain))
            con.commit()


def findPlayer(userName):
    con = connection()
    with con:
        with con.cursor() as cursor:
            sql = "SELECT * FROM `player` where name=%s"
            cursor.execute(sql, (userName,))
            result = cursor.fetchone()
            return result

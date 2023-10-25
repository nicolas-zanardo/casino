import pymysql.cursors
from Player import Player


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


def createPlayer(user_name, gain):
    con = connection()
    with con:
        with con.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `player` (`name`, `gain`) VALUES (%s, %s)"
            cursor.execute(sql, (user_name, gain))
            con.commit()


def findPlayer(username) -> Player | None:
    con = connection()
    with con:
        with con.cursor() as cursor:
            sql = "SELECT * FROM `player` where name=%s"
            cursor.execute(sql, (username,))
            player = cursor.fetchone()
            if player:
                name = player["name"]
                gain = player["gain"]
                id_user = player["id"]
                player = Player()
                player.setName(name)
                player.setGain(gain)
                player.setId(id_user)
            return player


def gainUpdate(player_stake: int, player: Player):
    con = connection()
    update_gain = player.getGain() - player_stake
    with con:
        with con.cursor() as cursor:
            sql = "UPDATE `player` SET `gain` = %s WHERE `id` = %s"
            cursor.execute(sql, (update_gain, player.getId()))
            con.commit()


def gainUpdateWin(gain_win: int, player: Player):
    con = connection()
    update_gain = player.getGain() + gain_win
    with con:
        with con.cursor() as cursor:
            sql = "UPDATE `player` SET `gain` = %s WHERE `id` = %s"
            cursor.execute(sql, (update_gain, player.getId()))
            con.commit()

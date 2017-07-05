import sqlite3 as sql

databaseName = "guildwars.db"
con = sql.connect(databaseName)

# run this for initial db setup or if a schema change has been made and you want to wipe everything.


def initDataBase():
    dropTables()
    createTables()

# USE AT YOUR OWN RISK, DROPS EVERYTHING


def dropTables():
    cur = con.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite%'")
    for row in cur.fetchall():
        query = "DROP TABLE IF EXISTS " + row[0]
        cur.execute(query)
        con.commit()


def createTables():
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS GW2_API_KEYS
    (DiscordID varchar(100) PRIMARY KEY, DiscordName varchar(100), GWAPIKey varchar(200), insertDate datetime)''')
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS continents (ItemID INTEGER PRIMARY KEY, ItemDescription varchar(200))''')
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS currencies (ItemID INTEGER PRIMARY KEY, ItemDescription varchar(200))''')
    con.cursor().execute(
        '''CREATE TABLE IF NOT EXISTS items (ItemID INTEGER PRIMARY KEY, ItemDescription varchar(200))''')
    con.commit()

# USE AT YOUR OWN RISK, DELETES ALL ROWS FROM ALL TABLES


def cleanTables():
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for row in cur:
        con.cursor().execute("DELETE FROM " + row[0])
        con.commit()


def insertQuery(tableName, itemID, itemDescription):
    con.cursor().execute("REPLACE INTO " + tableName +
                         " VALUES (?,?)", (itemID, itemDescription))
    con.commit()


def hasAPIKey(DiscordID):
    cur = con.cursor()
    cur.execute(
        "SELECT COUNT(1) FROM GW2_API_KEYS WHERE DiscordID = ?", (DiscordID,))
    if(cur.fetchone()[0] < 1):
        return False
    return True


def hasItem(itemID):
    cur = con.cursor()
    cur.execute("SELECT COUNT(1) FROM items WHERE ItemID = ?", (itemID,))
    if(cur.fetchone()[0] < 1):
        return False
    return True


def getAPIKey(DiscordID):
    cur = con.cursor()
    cur.execute(
        "SELECT GWAPIKey FROM GW2_API_KEYS WHERE DiscordID = ?", (DiscordID,))
    return cur.fetchone()[0]


def registerAPIKey(DiscordID, DiscordName, APIKey):
    cur = con.cursor()
    cur.execute("REPLACE INTO GW2_API_KEYS VALUES (?,?,?,date('now'))",
                (DiscordID, DiscordName, APIKey))
    con.commit()


def selectAllQuery(tableName):
    cur = con.cursor()
    cur.execute("SELECT * FROM " + tableName)
    data = cur.fetchall()
    return data


def countQuery(tableName):
    cur = con.cursor().execute("SELECT COUNT(1) FROM " + tableName)
    return cur.fetchone()[0]


def findItemByName(name):
    cur = con.cursor()
    cur.execute("SELECT * FROM items WHERE ItemDescription LIKE ?",
                ("%" + name.replace(" ", "%") + "%",))
    data = cur.fetchall()
    return data


def findItemNameByID(itemID):
    cur = con.cursor()
    cur.execute("SELECT ItemDescription FROM items WHERE ItemID = ?",
                (itemID,))
    data = cur.fetchall()
    return data[0]


def findCurrencyByName(name):
    cur = con.cursor()
    cur.execute("SELECT * FROM currencies WHERE ItemDescription LIKE ?",
                ("%" + name.replace(" ", "%") + "%",))
    data = cur.fetchall()
    return data

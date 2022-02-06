from func import*
from database_setup import*

def make_table_blitz():
    '''creates tables for players data and opening data for blitz'''
    try:
        mycursor.execute("drop table BlitzPlayers")
        mycursor.execute("drop table BlitzOpening")
    except:
        pass

    mycursor.execute("CREATE TABLE BlitzPlayers (BplayerID int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), name VARCHAR(50))")
    mycursor.execute("CREATE TABLE BlitzOpening (id int PRIMARY KEY AUTO_INCREMENT, color VARCHAR(50), moves VARCHAR(50) UNIQUE)")

def make_table_bullet():
    '''creates tables for players data and opening data for bullet'''
    try:
        mycursor.execute("drop table BulletPlayers")
        mycursor.execute("drop table BulletOpening")
    except:
        pass
    mycursor.execute("CREATE TABLE BulletPlayers (BplayerID int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), name VARCHAR(50))")
    mycursor.execute("CREATE TABLE BulletOpening (id int PRIMARY KEY AUTO_INCREMENT, color VARCHAR(50), moves VARCHAR(50) UNIQUE)")

def get_top_players_blitz():
    '''fetches the top players in blitz and puts the data in the database'''
    js=get_leaderboard_data()
    make_table_blitz()
    for i in range(len(js['live_blitz'])):
        val=js['live_blitz'][i]
        if 'name' in val:       ## as some players haven't mentioned their names, so we have not taken those entries (could be cheaters + i want names for display in visualizations ahead)
            mycursor.execute("INSERT INTO BlitzPlayers (username,name) VALUES (%s,%s)",(val['username'],val['name']))  
            db.commit()

def get_top_players_bullet():
    '''fetches the top players in bullet and puts the data in the database'''
    js=get_leaderboard_data()
    make_table_bullet()
    for i in range(len(js['live_bullet'])):
        val=js['live_bullet'][i]
        if 'name' in val:       
            mycursor.execute("INSERT INTO BulletPlayers (username,name) VALUES (%s,%s)",(val['username'],val['name']))  
            db.commit()

def make_junction_table_blitz():
    '''Creates junction tables for bullet game data
    It will drop the 2 tables(if present) and create them again after truncating the BlitzOpening table'''
    try:
        mycursor.execute("drop table BlitzJunctionW")
        mycursor.execute("drop table BlitzJunctionB")
    except:
        pass
    mycursor.execute('TRUNCATE BlitzOpening')
    mycursor.execute('''CREATE TABLE BlitzJunctionW (
                                                 BplayerID int NOT NULL, moveID int NOT NULL,count int NOT NULL,
                                                 PRIMARY KEY (BplayerID,moveID),
                                                 FOREIGN KEY (BplayerID) REFERENCES BlitzPlayers (BplayerID),
                                                 FOREIGN KEY (moveID) REFERENCES BlitzOpening (id) )''')
    mycursor.execute('''CREATE TABLE BlitzJunctionB (
                                                 BplayerID int NOT NULL, moveID int NOT NULL,count int NOT NULL,
                                                 PRIMARY KEY (BplayerID,moveID),
                                                 FOREIGN KEY (BplayerID) REFERENCES BlitzPlayers (BplayerID),
                                                 FOREIGN KEY (moveID) REFERENCES BlitzOpening (id) )''')


def make_junction_table_bullet():
    '''Creates junction tables for bullet game data
    It will drop the 2 tables(if present) and create them again after truncating the BulletOpening table'''
    
    try:
        mycursor.execute("drop table BulletJunctionW")
        mycursor.execute("drop table BulletJunctionB")
    except:
        pass
    mycursor.execute('TRUNCATE BulletOpening')
    mycursor.execute('''CREATE TABLE BulletJunctionW (
                                                 BplayerID int NOT NULL, moveID int NOT NULL,count int NOT NULL,
                                                 PRIMARY KEY (BplayerID,moveID),
                                                 FOREIGN KEY (BplayerID) REFERENCES BulletPlayers (BplayerID),
                                                 FOREIGN KEY (moveID) REFERENCES BulletOpening (id) )''')
    mycursor.execute('''CREATE TABLE BulletJunctionB (
                                                 BplayerID int NOT NULL, moveID int NOT NULL,count int NOT NULL,
                                                 PRIMARY KEY (BplayerID,moveID),
                                                 FOREIGN KEY (BplayerID) REFERENCES BulletPlayers (BplayerID),
                                                 FOREIGN KEY (moveID) REFERENCES BulletOpening (id) )''')


def get_top_moves_blitz(mingames=100):
    '''Selects the players from the top players table and finds the opening move played by them 
       and stores them into the database. For each player it fetches min 'mingames' no. of games. '''
    
    make_junction_table_blitz()
    mycursor.execute("SELECT * FROM BlitzPlayers")

    for x in mycursor:
        dicW, dicB={}, {}
        game_data_list=get_min_games(x[1], 'blitz', mingames)
        count=0
        for i in range(len(game_data_list)):

            try:
                move=get_opening_move(game_data_list[i],x[1])

            except:
                pass
            else:
                if move!=None:
                    if get_color(game_data_list[i],x[1])=='W':
                        dicW[move]= dicW.setdefault(move, 0)+1
                    else:
                        dicB[move]= dicB.setdefault(move, 0)+1
        
        for i in dicW.keys():
            try:
                cursorformoves.execute("INSERT INTO BlitzOpening (color,moves) VALUES (%s,%s)",('W',i))
                db.commit()
            except:
                pass
        for i in dicB.keys():
            try:
                cursorformoves.execute("INSERT INTO BlitzOpening (color,moves) VALUES (%s,%s)",('B',i))
                db.commit()
            except:
                pass
        for k,v in dicW.items():
            cursorformoves.execute("SELECT id FROM BlitzOpening WHERE moves=%s",(k,))
            mId=cursorformoves.fetchone()
            cursorformoves.execute("INSERT INTO BlitzJunctionW (BplayerID,moveid,count) VALUES (%s,%s,%s)",(x[0],mId[0],v))            
            db.commit()
        for k,v in dicB.items():
            cursorformoves.execute("SELECT id FROM BlitzOpening WHERE moves=%s",(k,))
            mId=cursorformoves.fetchone()
            cursorformoves.execute("INSERT INTO BlitzJunctionB (BplayerID,moveid,count) VALUES (%s,%s,%s)",(x[0],mId[0],v))            
            db.commit()


def get_top_moves_bullet(mingames=100):
    '''Selects the players from the top players table and finds the opening move played by them 
       and stores them into the database. For each player it fetches min 'mingames' no. of games. '''     
    make_junction_table_bullet()
    mycursor.execute("SELECT * FROM BulletPlayers")

    for x in mycursor:
        dicW, dicB={}, {}
        game_data_list=get_min_games(x[1], 'bullet', 100)
        count=0
        for i in range(len(game_data_list)):

            try:
                move=get_opening_move(game_data_list[i],x[1])

            except:
                pass
            else:
                if move!=None:
                    if get_color(game_data_list[i],x[1])=='W':
                        dicW[move]= dicW.setdefault(move, 0)+1
                    else:
                        dicB[move]= dicB.setdefault(move, 0)+1
        
        for i in dicW.keys():
            try:
                cursorformoves.execute("INSERT INTO BulletOpening (color,moves) VALUES (%s,%s)",('W',i))
                db.commit()
            except:
                pass
        for i in dicB.keys():
            try:
                cursorformoves.execute("INSERT INTO BulletOpening (color,moves) VALUES (%s,%s)",('B',i))
                db.commit()
            except:
                pass
        for k,v in dicW.items():
            cursorformoves.execute("SELECT id FROM BulletOpening WHERE moves=%s",(k,))
            mId=cursorformoves.fetchone()
            cursorformoves.execute("INSERT INTO BulletJunctionW (BplayerID,moveid,count) VALUES (%s,%s,%s)",(x[0],mId[0],v))            
            db.commit()
        for k,v in dicB.items():
            cursorformoves.execute("SELECT id FROM BulletOpening WHERE moves=%s",(k,))
            mId=cursorformoves.fetchone()
            cursorformoves.execute("INSERT INTO BulletJunctionB (BplayerID,moveid,count) VALUES (%s,%s,%s)",(x[0],mId[0],v))            
            db.commit()


def moves_frequency_BlitzW():
    '''It will provide us with the total count each of all the different moves played as white in Blitz'''
    dict_move={}
    cursorformoves = db.cursor(buffered=True)
    mycursor.execute("SELECT * FROM blitzopening WHERE color='W'")
    for x in mycursor:
        cursorformoves.execute("SELECT SUM(count) FROM BlitzJunctionW WHERE moveID=%s",(x[0],))
        for y in cursorformoves:
            dict_move[x[2]] = int(y[0])
    return dict(sorted(dict_move.items(),key= lambda x:x[1], reverse=True))

def moves_frequency_BlitzB():
    '''It will provide us with the total count each of all the different moves played as black in Blitz'''
    dict_move={}
    cursorformoves = db.cursor(buffered=True)
    mycursor.execute("SELECT * FROM blitzopening WHERE color='B'")
    for x in mycursor:
        cursorformoves.execute("SELECT SUM(count) FROM BlitzJunctionB WHERE moveID=%s",(x[0],))
        for y in cursorformoves:
            dict_move[x[2]] = int(y[0])
            
    return dict(sorted(dict_move.items(),key= lambda x:x[1], reverse=True))

def moves_frequency_BulletW():
    '''It will provide us with the total count each of all the different moves played as white in Bullet'''
    dict_move={}
    cursorformoves = db.cursor(buffered=True)
    mycursor.execute("SELECT * FROM bulletopening WHERE color='W'")
    for x in mycursor:
        cursorformoves.execute("SELECT SUM(count) FROM BulletJunctionW WHERE moveID=%s",(x[0],))
        for y in cursorformoves:
            dict_move[x[2]] = int(y[0])
    return dict(sorted(dict_move.items(),key= lambda x:x[1], reverse=True))

def moves_frequency_BulletB():
    '''It will provide us with the total count each of all the different moves played as black in Bullet'''
    dict_move={}
    cursorformoves = db.cursor(buffered=True)
    mycursor.execute("SELECT * FROM bulletopening WHERE color='B'")
    for x in mycursor:
        cursorformoves.execute("SELECT SUM(count) FROM BulletJunctionB WHERE moveID=%s",(x[0],))
        for y in cursorformoves:
            dict_move[x[2]] = int(y[0])
    return dict(sorted(dict_move.items(),key= lambda x:x[1], reverse=True))




if __name__ == "__main__":
    # get the records in the database of the opening chess moves by the top players
    get_top_players_blitz()
    get_top_players_bullet()
    get_top_moves_blitz(100)    # specify the min number of games to fetch the opening moves from for blitz games per player
    get_top_moves_bullet(100)   # specify the min number of games to fetch the opening moves from for bullet games per player

    #do note that the more the games the slower the fetching would be
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
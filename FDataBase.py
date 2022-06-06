import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False

        return True

    def addPost(self, user_id, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)", (user_id, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

    def deletePost(self, id_del):
        try:
            self.__cur.execute(f"delete from posts where id= '{id_del}'")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка удаления статьи из БД "+str(e))
            return False
        return True

    def likePost(self,  id_user_liked, id_liked_post):
        try:
            self.__cur.execute(f"SELECT * FROM likes where post_id='{id_liked_post}' and user_id='{id_user_liked}'")
            res = self.__cur.fetchone()
            if not res:
                self.__cur.execute(f"INSERT INTO likes VALUES(NULL, ?, ?, ?)", (id_user_liked, id_liked_post, 1))
            else:
                if res['isLike']:
                    self.__cur.execute(f"UPDATE likes SET isLike = 0 where post_id='{id_liked_post}' and user_id='{id_user_liked}'")
                else:
                    self.__cur.execute(
                        f"UPDATE likes SET isLike = 1 where post_id='{id_liked_post}' and user_id='{id_user_liked}'")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка при обработке лайка из БД "+str(e))
            return False
        return True

    def getLikesById(self, user_id):
        try:
            self.__cur.execute(f"SELECT * from likes where user_id = '{user_id}'")
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка при получении лайков из БД "+str(e))
            return False
        return res


    def getPosts(self):
        sql = '''SELECT * FROM posts'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []


    def getPostsById(self, user_id):
        sql = f'''SELECT * FROM posts WHERE user_id = '{user_id}';'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False


    def addDialog(self, id_user1, id_user2):
        try:
            self.__cur.execute(f"SELECT * FROM dialogs WHERE user_id1 = '{id_user1}' and user_id2 = '{id_user2}' or user_id1 = '{id_user2}' and user_id2 = '{id_user1}'")
            res = self.__cur.fetchone()
            if res:
                return
            self.__cur.execute(f"INSERT INTO dialogs VALUES(NULL, ?, ?)", (id_user1, id_user2))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления диалога в БД "+str(e))
            return False
        return True

    def addMessage(self, id_user1, id_user2, content):
        try:
            self.__cur.execute(f"INSERT INTO messages VALUES(NULL, ?, ?, ?)", (id_user1, id_user2, content))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления сообщения в БД "+str(e))
            return False
        return True

    def getPreferences(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM Preferences WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def getUsersByPreferences(self, mood, theme):
        try:
            self.__cur.execute(f"SELECT id, name from users where id in (SELECT id_user from Preferences where mood = '{mood}' and theme = '{theme}')")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def addAccepts(self, id_user1, id_user2):
        try:
            self.__cur.execute(f"INSERT INTO accepts VALUES(NULL, ?, ?)", (id_user1, id_user2))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления сообщения в БД "+str(e))
            return False
        return True

    def getNotifications(self, id_user):
        try:
            self.__cur.execute(f"SELECT a.id_user1 checkedid, c.name name from accepts a LEFT JOIN accepts b ON a.id_user1 = b.id_user2 and a.id_user2 = b.id_user1 JOIN users c ON a.id_user1 = c.id where b.id_user1 is null and a.id_user2 = '{id_user}'")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getMessagesForDialogs(self, id_user):
        try:
            self.__cur.execute(f"SELECT DISTINCT user_id1, user_id2 from messages where user_id1 = '{id_user}' or user_id2 = '{id_user}'")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def getAccepts(self, id_user1, id_user2):
        try:
            self.__cur.execute(f"SELECT id_user1, id_user2 from accepts where id_user1 = '{id_user1}' and id_user2 = '{id_user2}' or id_user1 = '{id_user2}' and id_user2 = '{id_user1}'")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False

    def addPreferences(self, id_user, mood, theme):
        try:
            if self.getPreferences(id_user):
                self.__cur.execute(f"UPDATE Preferences SET mood = ?, theme = ?  WHERE id_user = ?", (mood, theme, id_user))
            else:
                self.__cur.execute(f"INSERT INTO Preferences VALUES(NULL, ?, ?, ?)", (id_user, mood, theme))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления предпочтения в БД "+str(e))
            return False
        return True

    def getMessages(self, id_user1, id_user2):
        try:
            self.__cur.execute(f"SELECT content, name from messages JOIN users ON (messages.user_id1 = users.id) where user_id1 = '{id_user1}' and user_id2 = '{id_user2}' or user_id1 = '{id_user2}' and user_id2 = '{id_user1}'")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))


    def getDialog(self, id_user1, id_user2):
        try:
            self.__cur.execute(f"SELECT * from dialogs WHERE id_user1 = '{id_user1}' and id_user2 = '{id_user2}' or user_id1 = '{id_user2}' and user_id2 = '{id_user1}'")
            res = self.__cur.fetchone()
            return res
        except sqlite3.Error as e:
            print("Ошибка добавления диалога в БД "+str(e))
            return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: "+str(e))
            return False
        return True
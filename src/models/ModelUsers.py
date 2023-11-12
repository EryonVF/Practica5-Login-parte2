from .entities.users import User

class ModelUsers:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("call sp_verifyIdentity(%s, %s)", (user.username, user.password))
            row = cursor.fetchone()
            
            if row is not None:
                user = User(row[0], row[1], row[2], row[3], row[4])
                return user
            else:
                return None
        except Exception as ex:
            print("Error en el modelo de usuarios:", ex)
            raise
        finally:
            if cursor:
                cursor.close()

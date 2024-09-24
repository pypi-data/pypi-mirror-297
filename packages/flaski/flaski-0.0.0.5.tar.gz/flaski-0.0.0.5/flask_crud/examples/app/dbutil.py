
class DBController:
    mysql = None

    @staticmethod
    def checkMySQL():
        if not DBController.mysql:
            raise Exception("Asigne una instancia de MySQL a DBController.")
        return DBController.mysql

    @staticmethod
    def getColnames(table_name):
        mysql = DBController.checkMySQL()
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM {table_name} LIMIT 1"
        cursor.execute(query)
        column_names = [desc[0] for desc in cursor.description]
        return column_names

    @staticmethod
    def dict_fetch(cursor, one=False):
        """Convierte el resultado del cursor en un diccionario o lista de diccionarios"""
        columns = [col[0] for col in cursor.description]

        if one:
            row = cursor.fetchone()
            return dict(zip(columns, row)) if row else None
        else:
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def all(nametable):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            cursor.execute(f"SELECT * FROM {nametable}")
            result = DBController.dict_fetch(cursor)
            return result
        except Exception as e:
            raise Exception(f"Error al cargar TODOS los datos: {str(e)}")
        finally:
            cursor.close()

    @staticmethod
    def query(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            cursor.execute(query, args)
            result = DBController.dict_fetch(cursor, one=False)
            return result
        except Exception as e:
            raise Exception(f"Error al cargar los datos: {str(e)}")
        finally:
            cursor.close()

    @staticmethod
    def queryOne(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            cursor.execute(query, args)
            result = DBController.dict_fetch(cursor, one=True)
            return result
        except Exception as e:
            raise Exception(f"Error al cargar los datos: {str(e)}")
        finally:
            cursor.close()

    @staticmethod
    def update(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            result = cursor.execute(query, args)
            return result
        except Exception as e:
            msg = f"Error durante actualización de datos: {str(e)}"
            raise Exception(msg)
        finally:
            cursor.close()

    @staticmethod
    def delete(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            result = cursor.execute(query, args)
            return result
        except Exception as e:
            msg = f"Error al eliminar los datos: {str(e)}"
            raise Exception(msg)
        finally:
            cursor.close()


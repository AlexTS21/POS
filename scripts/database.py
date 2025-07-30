import sqlite3

class DataBase:
    def __init__(self, database):
        self.query = "" #String that will be the query
        self.database = database #nombre de la base
        pass
    
    def make_search_query(self, query, vars):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(query, vars)
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except Exception as e:
            print("Ocurrió un error al realizar el query:", e)
            return None
    
    def search(self, table, object, vars, strict=True):
        query = "SELECT " + ", ".join(vars)
        query += f" FROM {table} WHERE active = 1 AND ("
        union = "OR" if not strict else "AND"
        compar = "LIKE" if not strict else "="
        
        conditions = []
        values = []
        for k, v in object.items():
            if compar == "LIKE":
                conditions.append(f"{k} {compar} ?")
                values.append(f"%{v}%")  # Agrega comodines para LIKE
            else:
                conditions.append(f"{k} {compar} ?")
                values.append(v)
        
        query += f" {union} ".join(conditions)
        query += ")"

        results = self.make_search_query(query, values)

        res = []
        for r in results:
            aux = {}
            for k, v in zip(vars, r):
                aux[k] = v
            res.append(aux)
        
        return res
    
    def get_elemnts_on_table(self, table, vars, size=50):

        return
    
    def modify(self, table, key, value):
        """
        Updates one or more fields in a specific row of a table.

        Parameters:
            table (str): The name of the table.
            key (dict): Dictionary of conditions to locate the row (e.g., {"id": 5}).
            value (dict): Dictionary of fields to update (e.g., {"price": 9.99}).

        Returns:
            bool: True if at least one row was updated, False otherwise.
        """
        try:
            # Construir parte SET (valores a modificar)
            set_clause = ", ".join([f"{k} = ?" for k in value.keys()])
            set_values = list(value.values())

            # Construir parte WHERE (filtro por clave)
            where_clause = " AND ".join([f"{k} = ?" for k in key.keys()])
            where_values = list(key.values())

            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            values = set_values + where_values

            print("QUERY:", query)
            print("VALUES:", values)

            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            rowcount = cursor.rowcount
            conn.close()

            return rowcount > 0
        except Exception as e:
            print("Error during update:", e)
            return False


    #obect is a dic where key is the column of the table
    def insert(self, table, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = list(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(query, values)
            inserted_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return inserted_id
        except Exception as e:
            print("Error during insertion:", e)
            return False
        return
    
    #
    def delete(self, table, key, value):
        return


#db = DataBase("database.db")
#
#print(db.search("inventory", {"product_name": "Papel lustre"}, ["id", "product_name", "amount", "active"], strict=True))
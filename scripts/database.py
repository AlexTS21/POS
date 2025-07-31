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


    def get_today_cortes(self):
        query = """
            SELECT * FROM sales
            WHERE date(date) = date('now', 'localtime') AND active = 1;
            """

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()
    
        campos = ["id", "total_price", "cash", "change", "total_products", "user", "date", "active"]


        return [{k: v for k, v in zip(campos, r)} for r in resultados] if resultados else []


    def corte_realizado_hoy(self):
        query = """
            SELECT 1 FROM corte
            WHERE date(date) = date('now', 'localtime')
            LIMIT 1;
        """
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        conn.close()

        # Retorna True si encontró al menos un corte hoy, False si no
        return resultado is not None
    
    def get_detalles_venta(self, id_venta):
        query = """
            SELECT product_name, price, amount
            FROM salesDetail
            WHERE id_sale = ? AND active = 1;
        """
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(query, (id_venta,))
            rows = cursor.fetchall()
            conn.close()
            return [{"product_name": r[0], "price": r[1], "amount": r[2]} for r in rows]
        except Exception as e:
            print("Error al obtener detalles de venta:", e)
            return []
        
    def get_ultimos_cortes(self, limite=50):
        """
        Obtiene los cortes más recientes, hasta el número especificado por 'limite'.

        Parameters:
            limite (int): Número máximo de cortes a recuperar (por defecto 50).

        Returns:
            list[dict]: Lista de cortes con sus campos correspondientes.
        """
        query = f"""
            SELECT id, total, user, date, active
            FROM corte
            ORDER BY datetime(date) DESC
            LIMIT ?;
        """
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(query, (limite,))
            resultados = cursor.fetchall()
            conn.close()

            campos = ["id", "total", "user", "date", "active"]
            return [{k: v for k, v in zip(campos, r)} for r in resultados] if resultados else []
        except Exception as e:
            print("Error al obtener los últimos cortes:", e)
            return []


#db = DataBase("database.db")
#
#print(db.search("inventory", {"product_name": "Papel lustre"}, ["id", "product_name", "amount", "active"], strict=True))
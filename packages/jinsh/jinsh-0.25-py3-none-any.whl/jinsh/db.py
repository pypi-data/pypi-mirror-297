import oracledb
import json
from jinsh import tool


class oracle:
    pool = None
    def __int__(self, password, user="system", ip="138.2.104.103", port=1521,
                name="pdb1.sub07210521580.vcnzhdsgp.oraclevcn.com", min=1, max=3, increment=1):
        try:
            self.pool = oracledb.create_pool(
                user=user,
                password=password,
                dsn="%s:%s/%s" % (ip, port, name),
                min=min,
                max=max,
                increment=increment,
            )
            #return pool
        except Exception as e:
            print(e)
    def insert(self,sql, data):
        try:
            with self.pool.acquire() as connection:
                with connection.cursor() as cursor:
                    cursor.executemany(sql, data, )
                connection.commit()
            return tool.jsonMsg("success", data="", error="")
        except Exception as e:
            print(e)
            return tool.jsonMsg("fail", data="", error=str(e))
    def query(self, sql, data):
        try:
            with self.pool.acquire() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, data)
                    columns = [column[0] for column in cursor.description]
                    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    json_data = json.dumps(data)
                    return tool.jsonMsg("success", data=data, error="")
        except Exception as e:
            print(e)
            return tool.jsonMsg("fail", data="", error=str(e))

import oracledb
import json
from jinsh import tool
import contextlib
import numpy
import array

class oracle:
    pool = None
    def __init__(self, password, user="system", ip="138.2.104.103", port=1521,
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


class adb:

    def __init__(self, user, password, dsn, config_dir, wallet_location, wallet_password):
        conn = oracledb.connect(user=user, password=password, dsn=dsn,
                    config_dir=config_dir, wallet_location=wallet_location,
                    wallet_password=wallet_password)
        self.connection = conn

    def insert(self, sql, data):
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(sql, data, )
            self.connection.commit()
            return tool.jsonMsg("success", data="", error="")
        except Exception as e:
            print(e)
            return tool.jsonMsg("fail", data="", error=str(e))
    def query(self, sql, data):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, data)
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                json_data = json.dumps(data)
                return tool.jsonMsg("success", data=data, error="")
        except Exception as e:
            print(e)
            return tool.jsonMsg("fail", data="", error=str(e))

class db:
    pool = None
    def __init__(self,user,password,host,port,database):
        self.pool = oracledb.create_pool(user=user, password=password, dsn="{}:{}/{}".format(host, port, database), min=1, max=50, increment=1)

    def numpy_converter_in(self, value):
        if value.dtype == numpy.float64:
            dtype = "d"
        elif value.dtype == numpy.float32:
            dtype = "f"
        else:
            dtype = "b"
        return array.array(dtype, value)

    def input_type_handler(self, cursor, value, arraysize):
        if isinstance(value, numpy.ndarray):
            return cursor.var(
                oracledb.DB_TYPE_VECTOR,
                arraysize=arraysize,
                inconverter=self.numpy_converter_in,
            )

    def numpy_converter_out(self, value):
        if value.typecode == "b":
            dtype = numpy.int8
        elif value.typecode == "f":
            dtype = numpy.float32
        else:
            dtype = numpy.float64
        return numpy.array(value, copy=False, dtype=dtype)

    def output_type_handler(self, cursor, metadata):
        if metadata.type_code is oracledb.DB_TYPE_VECTOR:
            return cursor.var(
                metadata.type_code,
                arraysize=cursor.arraysize,
                outconverter=self.numpy_converter_out,
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass


    @contextlib.contextmanager
    def get_cursor(self):
        conn = self.pool.acquire()
        conn.inputtypehandler = self.input_type_handler
        conn.outputtypehandler = self.output_type_handler
        cur = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()
            conn.commit()
            conn.close()
    def query(self, sql, data):
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, data)
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                json_data = json.dumps(data)
                return tool.jsonMsg("success", data=data, error="")
        except Exception as e:
            print(e)
            return tool.jsonMsg("fail", data="", error=str(e))
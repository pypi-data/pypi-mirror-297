import os
import shutil_tools
from oracle_db import adb
def test():
    print("===获取当前文件目录===")
    # 当前脚本工作的目录路径
    print(os.getcwd())
    # os.path.abspath()获得绝对路径
    print(os.path.abspath(os.path.dirname(__file__)))

    print("=== 获取当前文件上层目录 ===")
    print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    print(os.path.abspath(os.path.dirname(os.getcwd())))
    print(os.path.abspath(os.path.join(os.getcwd(), "..")))
    print(os.path.dirname(os.getcwd()))
    # os.path.join()连接目录名与文件或目录


    print("==== 设置路径为当前文件上层目录的test_case文件夹====")
    path = os.path.join(os.path.dirname(os.getcwd()), "test_case")
    print(path)


def insert(db):
    sql = "insert into house(house_name,embedding,price,description) values (:1,vector(:2),:3,:4)"
    data = []
    data.append(("test", "[1,2,3]", "3", "nothing"))
    db.insert(sql, data)

def query(db):
    sql = "select * from house"
    data = []
    print(db.query(sql,data))

if __name__ == '__main__':
    #wallet_dir = "D:\\project\\code\\CLIP-search\\adb23c_tls_wallet"
    #dbpass=""
    #db = adb(user="admin", password=dbpass, dsn="myatp_medium", config_dir=wallet_dir, wallet_location=wallet_dir, wallet_password=dbpass)
    ##insert(db)
    #query(db)
    #print(shutil_tools.list_image_paths("C:\\Users\\wajin_cn\\Downloads\\105_classes_pins_dataset"))
    shutil_tools.show_selected_folders("C:\\Users\\wajin_cn\\Downloads\\105_classes_pins_dataset", ['pins_margot robbie'])

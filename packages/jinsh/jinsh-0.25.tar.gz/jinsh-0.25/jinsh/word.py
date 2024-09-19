import time

from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
import os
from gtts import gTTS
import pandas as pd
from jinsh import config
import shutil
class tool:
    engine = None
    def __init__(self):
        DBHOST = os.environ.get(config.DBHOST)
        DBUSER = os.environ.get(config.DBUSER)
        PASSWORD = os.environ.get(config.DBPASS)
        DB = os.environ.get(config.DBNAME)
        self.engine = create_engine(
            'mysql+pymysql://{DBUSER}:{PASSWORD}@{DBHOST}/{DB}'.format(DBUSER=DBUSER, PASSWORD=PASSWORD,
                                                                        DBHOST=DBHOST,DB=DB))
    def dftmysql(self,excel_path='/Users/walter/Documents/newwords.xlsx',sheet_name='cyber',table_name='cyber_words_temp',type='replace'):
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        df.head()
        df.to_sql(con=self.engine, name=table_name, if_exists=type)
    def generateAudio(self,audio_path = "/data/work/tts/",query_sql="select word,translation,unit from cyber_words_temp where unit like 'He%'"):
        audio_location = audio_path
        SessionFactory = sessionmaker(bind=self.engine)
        session = SessionFactory()
        sql=text(query_sql)
        words = session.execute(sql).fetchall()
        unit_words = []
        title = ""
        init_flag = True
        for word_tuple in words:
            word = word_tuple[0]
            translation = word_tuple[1]
            title = word_tuple[2]
            unit_folder = audio_location + "/" + title
            if init_flag:
                if os.path.exists(unit_folder):
                    #os.rmdir(unit_folder)
                    shutil.rmtree(unit_folder, ignore_errors=True)
                    os.makedirs(unit_folder)
                else:
                    os.makedirs(unit_folder)
                init_flag = False

            if os.path.exists(unit_folder+"/%s.mp3" % (word,)):
                print("Englist word file already exists, skip this one.")
            else:
                gTTS(text=word, lang='en', tld='us').save("%s/%s.mp3" % (unit_folder,word))
                time.sleep(1)
            if os.path.exists(unit_folder + "/%s_cn.mp3" % (word,)):
                print("Translation file already exists, skip this one.")
            else:
                gTTS(text=translation, lang='zh-CN').save("%s/%s_cn.mp3" % (unit_folder, word))
                time.sleep(1)
            #gTTS(text=word, lang='en', tld='us').save("%s/%s.mp3" % (unit_folder, word))
            #gTTS(text=translation, lang='zh-CN').save("%s/%s_cn.mp3" % (unit_folder, word))
            word_path = "{}.mp3".format(word, )
            unit_words.append(word_path)
            word_cn_path = "{}_cn.mp3".format(word, )
            unit_words.append(word_cn_path)

        ffmpeg_cmd = ['ffmpeg', '-i', '"concat:' + '|'.join(unit_words) + '"', '-c', 'copy', '"../' + str(title) + '.mp3"']
        print(" ".join(ffmpeg_cmd))
        os.chdir(unit_folder)
        os.system(" ".join(ffmpeg_cmd))
        #self.generateList(self, query_sql)
    def generateList(self,query_sql):
        audio_location = os.getcwd()
        SessionFactory = sessionmaker(bind=self.engine)
        session = SessionFactory()
        sql=text(query_sql)
        words = session.execute(sql).fetchall()
        unit_words = []
        title = ""
        for word_tuple in words:
            word = word_tuple[0]
            word_path = "{}.mp3".format(word, )
            unit_words.append(word_path)
            word_cn_path = "{}_cn.mp3".format(word, )
            unit_words.append(word_cn_path)
            title = word_tuple[1]
        ffmpeg_cmd = ['ffmpeg', '-i', '"concat:' + '|'.join(unit_words) + '"', '-c', 'copy','"'+str(title)+'.mp3"']
        print(" ".join(ffmpeg_cmd))

if __name__ == "__main__":
    #generateList("select word,unit from cyber_words_temp where unit like 'He%'")
    t = tool()
    t.generateAudio()
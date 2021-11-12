import time

import kivy
import numpy as np
import pandas as pd
import datetime
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget

kivy.require('1.10.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.core.window import Window

import matplotlib.pyplot as plt
import sqlite3 as sl

class MenuScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class CredentialsScreen(Screen):
    registered = {}
    con = sl.connect('google_fit.db')
    data = con.execute("SELECT mail,password FROM USER")
    for row in data:
        registered[row[0]]=row[1]
    con.close()

    def comprovar_mail(self, mail):
        try:
            if self.registered[mail]:
                return True
            else:
                return False
        except:
            return False

    def comprovar(self, mail, password):
        try:
            if self.registered[mail] == password:
                app = App.get_running_app()
                app.mail = mail
                return True
            else:
                return False
        except:
            return False


class NewScreen(Screen):

    def comprovar(self, age, gender, weight, height, mail, password):
        nulls = [None, '', np.NAN]
        if age not in nulls and age!='Type your age' and gender not in nulls and gender in 'wmWM' and weight not in nulls and weight!='Type your weight' and height not in nulls and height!='Type your height' and mail not in nulls and mail!='Type your mail' and password not in nulls and password!='Type your password'\
                and age.isnumeric() and weight.isnumeric() and height.isnumeric() and '@' in mail and '.' in mail:
            app = App.get_running_app()
            app.mail = self.ids.mail.text
            return True
        else:
            return False
    def insertar(self,name,surname,gender,age, weight, height, mail, password):
        con = sl.connect('google_fit.db')
        con.executemany('INSERT INTO USER (name, surname,gender, age, weight, height, mail, password) values(?, ?,?, ?, ?, ?, ?, ?)', [(name, surname, gender, int(age), int(weight), int(height), mail, password)])
        con.commit()
        con.close()

class ProfileScreen(Screen):

    image_path = 'empty_profile.jpg'
    img = mpimg.imread(image_path)
    imgplot = plt.imshow(img)

    filename = 'finalized_model.sav'
    model = pickle.load(open(filename, 'rb'))

    #TODO que toda la info del user venga automatica
    email = 'alice@gmail.com'
    user = 1

    my_progress = 0
    to_walk = 0
    dict_rec = {'16':10, '17':15, '20':30, '27':45, '30':60}
    BMI = 0
    celebration = False
    count = 0
    data = pd.DataFrame()
    name_user = StringProperty()

    def cargar_datos_vacios(self):
        self.my_progress=0
        con = sl.connect('google_fit.db')
        df_user = pd.read_sql_query("SELECT * FROM USER", con)
        app = App.get_running_app()
        df_user = df_user[df_user['mail']==app.mail]
        try:
            self.user = df_user['id'][0]
            self.BMI = float(df_user['weight'][0])/(df_user['height'][0]/100)**2
            if df_user['gender'].values[0] in 'wW':
                if df_user['age'].values[0] < 40:
                    self.name_user = 'Miss ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
                else:
                    self.name_user = 'Mrs. ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
            else:
                if df_user['age'].values[0] < 40:
                    self.name_user = 'Sir ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
        except:
            self.user = 1

        con.close()
        self.image_path = 'empty_profile.png'
        return self.image_path, round(self.BMI,1)

    def cargar_datos(self):

        con = sl.connect('google_fit.db')
        df = pd.read_sql_query("SELECT * FROM DATA", con)
        df_user = pd.read_sql_query("SELECT * FROM USER", con)
        app = App.get_running_app()
        df_user = df_user[df_user['mail'] == app.mail]

        self.user = df_user['id'].values[0]
        if df_user['gender'].values[0] in 'wW':
            if df_user['age'].values[0] < 40:
                self.name_user = 'Miss ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
            else:
                self.name_user = 'Mrs. ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
        else:
            if df_user['age'].values[0] < 40:
                self.name_user = 'Sir ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]

        self.BMI = float(df_user['weight'].values[0]) / (df_user['height'].values[0] / 100) ** 2
        self.BMI = round(self.BMI, 1)
        self.data = df[df['id'] == self.user]
        if self.data.shape[0]==0:
            return self.cargar_datos_vacios()
        else:
            #TODO respecto el total esperado

            if self.BMI<16:
                key='16'
            elif self.BMI<18.5:
                key = '17'
            elif self.BMI < 25:
                key = '20'
            elif self.BMI < 30:
                key = '27'
            else:
                key = '30'
            self.to_walk = self.dict_rec[key]
            self.my_progress = (self.data["walking"].sum()/60)*15/self.to_walk
            fig = plt.figure(figsize=(15, 10), facecolor='#faf5e5')
            ax = fig.add_subplot(1, 1, 1)

            labels = ["Walking", "Car", "Train", "Still", "Bus"]

            ax.set_title("Activities distribution", fontsize=40)

            ax.pie([self.data["walking"].sum(), self.data["car"].sum(), self.data["train"].sum(), \
                    self.data["still"].sum(), self.data["bus"].sum()], normalize=True, \
                   labels=labels, autopct=lambda p: '{:.1f}%'.format(p), textprops={'fontsize': 25})
            now = str(datetime.datetime.now()).replace(' ','').replace('-','').replace('.','').replace(':','')

            plt.savefig(f"./images/pie_chart_{now}.png")
            con.close()

            self.image_path = f"./images/pie_chart_{now}.png"

            return  self.image_path,self.BMI

    def refresh_data(self):

        con = sl.connect('google_fit.db')
        df = pd.read_sql_query("SELECT * FROM DATA", con)
        df_user = pd.read_sql_query("SELECT * FROM USER", con)
        app = App.get_running_app()
        df_user = df_user[df_user['mail'] == app.mail]

        self.user = int(df_user['id'].values[0])
        if df_user['gender'].values[0] in 'wW':
            if df_user['age'].values[0] < 40:
                self.name_user = 'Miss ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
            else:
                self.name_user = 'Mrs. ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
        else:
            if df_user['age'].values[0] < 40:
                self.name_user = 'Sir ' + df_user['name'].values[0] + ' ' + df_user['surname'].values[0]
        print(self.name_user)
        if self.count == 0:
            #TODO info coming from sensors
            new_info = pd.read_csv('test_U11.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(self.user,datetime.datetime.now(),np.count_nonzero(y_pred == 4),np.count_nonzero(y_pred == 1),np.count_nonzero(y_pred == 2),np.count_nonzero(y_pred == 3),np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            con.close()
            self.count += 1
        elif self.count == 1:
            new_info = pd.read_csv('test_U9.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(self.user, datetime.datetime.now(), np.count_nonzero(y_pred == 4), np.count_nonzero(y_pred == 1),
                               np.count_nonzero(y_pred == 2), np.count_nonzero(y_pred == 3),
                               np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            con.close()
            self.count += 1
        elif self.count == 2:
            new_info = pd.read_csv('test_U5.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(self.user, datetime.datetime.now(), np.count_nonzero(y_pred == 4), np.count_nonzero(y_pred == 1),
                               np.count_nonzero(y_pred == 2), np.count_nonzero(y_pred == 3),
                               np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            con.close()
            self.count += 1
        elif self.count == 3:
            new_info = pd.read_csv('test_U2.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(self.user, datetime.datetime.now(), np.count_nonzero(y_pred == 4), np.count_nonzero(y_pred == 1),
                               np.count_nonzero(y_pred == 2), np.count_nonzero(y_pred == 3),
                               np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            con.close()
            self.count += 1
        else:
            self.count = 0

        if self.my_progress >= 100:
            self.celebration = True
        return self.cargar_datos()



"""
class ThirdScreen(Screen):
    def starttimer(self):
        self.timer = Clock.schedule_once(self.screen_switch_four, 6)
    def screen_switch_four(self, dt):
        self.manager.current = 'fourth_screen'
"""

class MainApp(App):

    user = 0
    nombre_usuario = ''
    apellido_usuario = ''
    mail = ''

    def build(self):

        return Builder.load_file('Main.kv')

if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    MainApp().run()
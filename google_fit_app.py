import kivy
import numpy as np
import pandas as pd
import datetime
import pickle

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
            app.mail = mail
            return True
        else:
            return False
    def insertar(self,name,surname,gender,age, weight, height, mail, password):
        con = sl.connect('google_fit.db')
        con.executemany('INSERT INTO USER (name, surname,gender, age, weight, height, mail, password) values(?, ?,?, ?, ?, ?, ?, ?)', [(name, surname, gender, int(age), int(weight), int(height), mail, password)])
        con.commit()
        con.close()

class ProfileScreen(Screen):

    filename = 'finalized_model.sav'
    model = pickle.load(open(filename, 'rb'))

    #TODO que toda la info del user venga automatica
    email = 'alice@gmail.com'
    user = 1


    my_progress = 0
    celebration = False
    count = 0
    data = pd.DataFrame()

    def refresh_data(self):
        con = sl.connect('google_fit.db')
        df = pd.read_sql_query("SELECT * FROM DATA", con)
        df_user = pd.read_sql_query("SELECT * FROM USER", con)
        if self.count == 0:
            new_info = pd.read_csv('test_U11.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(1,datetime.datetime.now(),np.count_nonzero(y_pred == 4),np.count_nonzero(y_pred == 1),np.count_nonzero(y_pred == 2),np.count_nonzero(y_pred == 3),np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            self.count += 1
        elif self.count == 1:
            new_info = pd.read_csv('test_U9.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(1, datetime.datetime.now(), np.count_nonzero(y_pred == 4), np.count_nonzero(y_pred == 1),
                               np.count_nonzero(y_pred == 2), np.count_nonzero(y_pred == 3),
                               np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            self.count += 1
        elif self.count == 2:
            new_info = pd.read_csv('test_U5.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(1, datetime.datetime.now(), np.count_nonzero(y_pred == 4), np.count_nonzero(y_pred == 1),
                               np.count_nonzero(y_pred == 2), np.count_nonzero(y_pred == 3),
                               np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            self.count += 1
        elif self.count == 3:
            new_info = pd.read_csv('test_U2.csv')
            y_pred = self.model.predict(new_info)

            data_to_insert = [(1, datetime.datetime.now(), np.count_nonzero(y_pred == 4), np.count_nonzero(y_pred == 1),
                               np.count_nonzero(y_pred == 2), np.count_nonzero(y_pred == 3),
                               np.count_nonzero(y_pred == 0))]
            con.executemany(
                'INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
            con.commit()
            self.count += 1
        if self.my_progress >= 100:
            self.celebration = True

        self.data = df[df['id'] == self.user]


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
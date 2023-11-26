from flask import Flask
from flask import render_template, url_for, flash, request, redirect, Response
import sqlite3
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms import LoginForm

@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('/var/www/flask/login.db')
   curs = conn.cursor()
   curs.execute("SELECT * from login where id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])
#
#   Copyright (C) 2023 Midn1ght
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import redis
from flask import Flask, session, redirect, url_for, request, render_template, g
import random
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from pizzapi import *
import sqlite3
import os

DATABASE = 'pizza.db'

app = Flask(__name__)
store = RedisStore(redis.StrictRedis())
KVSessionExtension(store, app)
app.secret_key = os.urandom(32)

random_msg = random.choice(["No.", "It is pointless.", "You can leave now.", "-._-.", "You shall not pass!", "Skill issue.", "Y'know, trying to ruin all the fun for everyone is just lame. Why not go outside, maybe get a life or something, will ya?"])

def remove(string):
    return string.replace(" ", "")

usrSelect = None

@app.route('/login', methods=["GET", "POST"])
def login():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        # rm: return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    if request.method == "POST":
        session['name'] = request.form['name']
        session['password'] = request.form['password2']
        usrname = remove(session['name'])
        password = remove(session['password'])
        global stuff
        stuff = [usrname, password]
        if usrname == "":
            return "<script>alert('Missing info! Aborting...'); window.location.href='/'</script>"
        if password == "":
            return "<script>alert('Missing info! Aborting...'); window.location.href='/'</script>"
        table_name = 'users'
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(f"select * from users where user_name = '{usrname}' and user_password = '{password}';")
        if not c.fetchone():
            session.clear()
            return "<script>alert('Error: Username or password invalid.'); window.location.href='/';</script>"
        conn.commit()
        print("[log]: user logged in -->", usrname)
        return redirect(url_for('index'))
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <a href="/">Back</a>
    <img id="mii-image" align="right" src="">
    <a> </a>
    <a> </a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
    <br>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <form class="center" id="get" "action="" method="post">
  <h2>Login</h2>
    <label for="name">Enter your username:</label><br>
    <input type="text" id="name" name="name" maxlength="10" required><br>
    <label for="password">Enter your password:</label><br>
    <input type="password" id="password2" name="password2" required><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
'''

@app.route('/signout', methods=["GET", "POST"])
def signout():
    print("[log]: user has logged out -->", remove(session['name']))
    session.clear()
    return "<script>window.location.href='/';</script>"

@app.route("/", methods=["GET", "POST"])
def index():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        # rm: return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute(f"select user_name = '{remove(session['name'])}' and user_password = '{remove(session['password'])}' from users")
        if not c.fetchone():
            pass
        else:
            return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
<style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
    
    .center2 {
      margin: 0;
      position: absolute;
      top: 50%;
      left: 50%;
      -ms-transform: translate(-50%, -50%);
      transform: translate(-50%, -50%);
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a href="faq">?</a>
    <a> </a>
    <a> </a>
    <a> </a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <br><br><br><br><br><br><br>
  <h1 class="center">Welcome to Macchiiato!</h1>
  <p class="center">To get started, make an account or login!</p>
  <div class="container">
    <div class="center2">
      <button onclick="window.location.href='/start'">Start ordering!</button>
      <button onclick="window.location.href='/signout'">Sign out!</button>
    </div>
  </div>
  </div>
</body>
</html>
'''
    except Exception as e:
        print(e)
        pass
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
<style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
    
    .center2 {
      margin: 0;
      position: absolute;
      top: 50%;
      left: 50%;
      -ms-transform: translate(-50%, -50%);
      transform: translate(-50%, -50%);
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a href="faq">?</a>
    <a> </a>
    <a> </a>
    <a> </a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <br><br><br><br><br><br><br>
  <h1 class="center">Welcome to Macchiiato!</h1>
  <br>
  <p class="center">To get started, make an account or login!</p>
  <div class="container">
    <div class="center2">
      <button onclick="window.location.href='/login'">Login!</button>
      <button onclick="window.location.href='/signup'">Sign up!</button>
    </div>
  </div>
  </div>
</body>
</html>
'''

@app.route('/faq')
def faq():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        # rm: return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"    
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
<style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
    
    .center2 {
      margin: 0;
      position: absolute;
      top: 50%;
      left: 50%;
      -ms-transform: translate(-50%, -50%);
      transform: translate(-50%, -50%);
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <br>
    <a href="/">Back</a>
    <a> </a>
    <a> </a>
    <a> </a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <h1 class="center">Info</h1>
  <p class="center"> Macchiiato is a web app project consisting of quality of life services that you load on TVii. <br> As of now, one of these services called <b>Munchiies</b> is in public beta, for which said service allows you to order Domino's Pizza straight from your Wii U (as of now, US only)!
  <h2 class="center"><b>So, what will you be able to order?</b></h2>
  <p class="center">Whatever you can order from Domino's Pizza. <br> A downside, however, is that pizzapi (the python package) only supports the US.</p>

  <h2 class="center"><b>Will rehosts be allowed? pretty pls :pleading:</b></h2>
  <p class="center">Yes, once I make a proper guide to doing so.</p>

  <h2 class="center"><b>Will you ever support other regions that aren't the US?</b></h2>
  <p class="center">Quite possibly, I will at least look into it at some point.</p>
  <h2 class="center"><b>Wii (as in me myself lol), will be taking feedback very seriously.<br> If you have any other questions, comments, or concerns, <br> don't be afraid to talk to me (@midn1ghthacker on discord).</b></h2>
  <h2 class="center">:))))))))))))))))))))))))))))</h2>
  </div>
  </div>
</body>
</html>
'''

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        # rm: return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    if request.method == "POST":
        usrname = remove(request.form['usrname'])
        password = remove(request.form['password'])
        email = remove(request.form['email'])
        phone = remove(request.form['phone'])
        phone = ''.join(i for i in phone if i.isdigit())
        if usrname == "":
            return "<script>alert('Missing info! Aborting...'); window.location.href='/'</script>"
        if password == "":
            return "<script>alert('Missing info! Aborting...'); window.location.href='/'</script>"
        if email == "":
            return "<script>alert('Missing info! Aborting...'); window.location.href='/'</script>"
        if phone == "":
            return "<script>alert('Missing info! Aborting...'); window.location.href='/'</script>"
        table_name = 'users'
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            sql = 'create table if not exists ' + table_name + ' (user_id integer primary key autoincrement, user_name text unique, user_password text not null, user_email text unique, user_phone text unique, user_street text unique, user_state text, user_city text, user_zip integer)'
            c.execute(sql)
        except:
            return "<script>alert('Error: User or info within request already exists in the server.'); window.location.href='/';</script>"
        params = (usrname, password, email, phone, "NULL", "NULL", "NULL", "NULL")
        try:
            c.execute('insert into ' + table_name + ' (user_name, user_password, user_email, user_phone, user_street, user_state, user_city, user_zip) values (?, ?, ?, ?, ?, ?, ?, ?)', params)
            conn.commit()
            print("[log]: created new user -->", usrname)
        except Exception as e:
            print(e)
            return "<script>alert('Error: User or info within request already exists in the server.'); window.location.href='/';</script>"
        return "<script>alert('Successfully created new user!'); window.location.href='/login';</script>"
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a href="/">Back</a>
    <a> </a>
    <a> </a>
    <a> </a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
    <br>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <form class="center" id="get" "action="" method="POST">
  <h2>Sign Up</h2>
    <label for="name">Enter your username:</label><br>
    <input type="text" id="usrname" name="usrname" maxlength="10" required><br>
    <label for="password">Enter your password:</label><br>
    <input type="password" id="password" name="password" minlength="4" required><br>
    <label for="email">Enter your email:</label><br>
    <input type="text" id="email" name="email" required><br>
    <label for="phone">Enter your phone number:</label><br>
    <input type="text" id="phone" name="phone" required><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
'''

@app.route('/start', methods=["GET", "POST"])
def start():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        # rm: return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    #usrName = session['name']
    password = session['password']
    table_name = 'users'
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute(f"select user_name = user_name and user_street = NULL and user_city = NULL and user_state = NULL and user_zip = NULL from users")
    except:
        return "<script>alert('User not logged in! Is this a bug? If so, please report it on the discord server.');</script>"
    result = c.fetchone()
    if result:
        pass
    else:
        return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <script>
    var bButtonCheck = setInterval(function() {
      wiiu.gamepad.update();
      if(wiiu.gamepad.hold === 16384) {
       document.getElementById("back-msg").innerHTML = '<div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">Returning to previous page...</div>';
       vino.soundPlayEx('SE_HTML_CANCEL_TOUCH_OFF', 1);
       window.location.href = '/';
      }
    });
  </script>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a class="active">Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a>Select Food</a>
    <a> </a>
    <a> </a>
    <a>Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
    <br>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  <div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">(B): Back</div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <a href='/menu'><h2 class="center">Continue</h2></a>
  <a href='/start2>Change address info</a>
</body>
</html>
''' 
    if request.method == 'POST':
        global street
        global city
        global state
        global zipcode
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['postalcode']
        a = 0
        if street == "":
            a = a + 1
        if city == "":
            a = a + 1
        if state == "":
            a = a + 1
        if zipcode == "":
            a = a + 1
        if a == 4 >= 0:
            return "<script>alert('Missing info.'); window.location.href='/start'</script>"
        else:
            pass
        params = (str(password), str(street), str(city), str(state), int(zipcode))
        print(params)
        try:
            c.execute('insert into ' + table_name + ' (user_password, user_street, user_city, user_state, user_zip) values (?, ?, ?, ?, ?)', params)
            conn.commit()
        except Exception as e:
            print(e)
            return "<script>alert('not logged in or other error'); window.location.href='/'</script>"
        global address
        address = Address(street, city, state, zipcode)
        return redirect(url_for('menu'))
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <script>
    var bButtonCheck = setInterval(function() {
      wiiu.gamepad.update();
      if(wiiu.gamepad.hold === 16384) {
       document.getElementById("back-msg").innerHTML = '<div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">Returning to previous page...</div>';
       vino.soundPlayEx('SE_HTML_CANCEL_TOUCH_OFF', 1);
       window.location.href = '/';
      }
    });
  </script>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a class="active">Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a>Select Food</a>
    <a> </a>
    <a> </a>
    <a> </a>
    <a>Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
    <br>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  <div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">(B): Back</div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <form class="center" id="get" "action="" method="post">
  <h2>Address Info</h2>
    <label for="street">Enter your street:</label><br>
    <input type="text" id="street" name="street" required><br>
    <label for="state">Enter your state:</label><br>
    <input type="state" id="state" name="state" required><br>
    <label for="city">Enter your city:</label><br>
    <input type="text" id="city" name="city" required><br>
    <label for="postalcode">Enter your ZIP code</label><br>
    <input type="text" id="postalcode" name="postalcode" required><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
'''

@app.route('/start2', methods=["GET", "POST"])
def start2():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        # rm: return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    #usrName = session['name']
    password = session['password']
    table_name = 'users'
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if request.method == 'POST':
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['postalcode']
        a = 0
        if street == "":
            a = a + 1
        if city == "":
            a = a + 1
        if state == "":
            a = a + 1
        if zipcode == "":
            a = a + 1
        if a == 0 <= 4:
            return "<script>alert('Missing info.'); window.location.href='/start2'</script>"
        params = (password, street, city, state, zipcode)
        params2 = (password, 'NULL', 'NULL', 'NULL', 'NULL')
        try:
            c.execute('insert into ' + table_name + ' (user_password, user_street, user_city, user_state, user_zip) values (?, ?, ?, ?, ?)', params)
            conn.commit()
        except Exception as e:
            print(e)
            return "<script>alert('not logged in or other error'); window.location.href='/'</script>"
        a = c.execute("select user_street and user_city and user_state and user_zip from users")
        resulty = a.fetchall()
        street = resulty[0]
        city = resulty[1]
        state = resulty[2]
        zipcode = resulty[3]
        print(state)
        try:
            global address
            address = Address(street, city, state, zipcode)
        except Exception as e:
            print(e)
            c.execute('insert into ' + table_name + ' (user_password, user_street, user_city, user_state, user_zip) values (?, ?, ?, ?, ?)', params2)
            conn.commit()
            return "<script>alert('Invalid info...'); window.location.href='/start2'</script>"
        return redirect(url_for('start'))
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <script>
    var bButtonCheck = setInterval(function() {
      wiiu.gamepad.update();
      if(wiiu.gamepad.hold === 16384) {
       document.getElementById("back-msg").innerHTML = '<div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">Returning to previous page...</div>';
       vino.soundPlayEx('SE_HTML_CANCEL_TOUCH_OFF', 1);
       window.location.href = '/';
      }
    });
  </script>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a class="active">Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a>Select Food</a>
    <a> </a>
    <a> </a>
    <a>Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
    <br>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  <div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">(B): Back</div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <form class="center" id="get" "action="" method="post">
  <h2>Address Info</h2>
    <label for="street">Enter your street:</label><br>
    <input type="text" id="street" name="street" required><br>
    <label for="state">Enter your state:</label><br>
    <input type="state" id="state" name="state" required><br>
    <label for="city">Enter your city:</label><br>
    <input type="text" id="city" name="city" required><br>
    <label for="postalcode">Enter your ZIP code</label><br>
    <input type="text" id="postalcode" name="postalcode" required><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
'''

@app.route('/menu', methods=["GET", "POST"])
def menu():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        # rm: return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    try:
        global store
        store = address.closest_store()
    except Exception as e:
        print(e)
        return '<script>alert("' + str(e) + '"); window.location.href="/start";</script>'
    if request.method == 'POST':
        fn = request.form['firstname']
        ln = request.form['lastname']
        
        session['firstname'] = remove(fn)
        session['lastname'] = remove(ln)
        
        global customer
        customer = Customer(session['firstname'], session['lastname'], session['email'], session['phone'])
        return redirect(url_for('menu2'))
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <script>
    alert("Nearest store successfully auto-selected.");
    var bButtonCheck = setInterval(function() {
      wiiu.gamepad.update();
      if(wiiu.gamepad.hold === 16384) {
       document.getElementById("back-msg").innerHTML = '<div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">Returning to previous page...</div>';
       vino.soundPlayEx('SE_HTML_CANCEL_TOUCH_OFF', 1);
       window.location.href = '/';
      }
    });
  </script>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a class="active">Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a>Select Food</a>
    <a> </a>
    <a> </a>
    <a>Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
    <br>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  <div id="back-msg" style="font-size:18px; position: fixed; bottom: 6px; left: 50px; z-index: 5;">(B): Back</div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <form class="center" id="get" "action="" method="post">
  <h2>Name Info</h2>
    <label for="firstname">Enter your First Name for this order:</label><br>
    <input type="text" id="firstname" name="firstname" required><br>
    <label for="lastname">Enter your Last Name for this order:</label><br>
    <input type="lastname" id="lastname" name="lastname" required><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
'''

@app.route('/menu2', methods=['GET', 'POST'])
def menu2():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    try:
        global order
        order = Order(store, customer, address)
        menu = store.get_menu()
        entry = menu.search(Code=str(usrSelect))
        laMenu = menu.search()
    except Exception as e:
        print(e)
        return '<script>alert("' + str(e) + '"); window.location.href="/start";</script>'
    else:
        return '<script>alert("err! missing details."); window.location.href="/start";</script>'
    
        if 'usrSelect' in session:
            try:
                session['usrSelect'] = request.form['usrSelect']
                usrSelect = session['usrSelect']
                order.add_item(usrSelect)
            except Exception as e:
                return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <script>alert(''' + str(e) + ''');</script>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a>Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a class="active">Select Food</a>
    <a> </a>
    <a> </a>
    <a>Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <h1 class="center">Select Food</h1>
  <br>
  <script>
    function addItems() {
    var content = document.getElementById("usrSelect");
    var selMenu = document.getElementById("selected-item-menu");
    selMenu.innerHTML = content.innerHTML + '<h5>''' + " " + '''</h5>';
    };

    function minItems() {
    var content = document.getElementById("usrSelect");
    var selMenu = document.getElementById("selected-item-menu");
    if (selMenu.innerHTML === " ") {
      alert("No items to remove.");
    }
    var selMenu.innerHTML = content.innerHTML - '<h5>''' + " " + '''</h5>';
    };
  </script>
  <div id="menu">
    <h3>Menu:</h3>
    ''' + str(laMenu) + '''
  </div>
  <div id="selected-item-menu">
    <h3>Selected items:</h3>
    ''' + str(usrSelect) + '''
  </div>
  <br>
    <h2>Add items to order:</h2>
    <form style="text-align:left;" id="sel" "action="addItems();" method="post">
      <div style="overflow: hidden; padding-right: .5em;">
          <input type="submit" value="Add" style="float: right" />
          <input type="text" style="width: 100%;" id="usrSelect" name="usrSelect" placeholder="Enter item code (code on the left of an item) to add to order"><br>
      </div>
    </form>
  <br>
  <h2>Remove items from order:</h2>
  <form style="text-align:left;" id="sel2" "action="minItems();" method="post">
      <div style="overflow: hidden; padding-right: .5em;">
          <input type="submit" value="Remove" style="float: right" />
          <input type="text" style="width: 100%;" id="usrSelect" name="usrSelect" placeholder="Enter item code (code on the left of an item) to remove from order"><br>
      </div>
      <br>
      <br>
  </form>
</body>
</html>
'''
        if 'usrDeselect' in session:
            try:
                session['usrDeselect'] = request.form['usrDeselect']
                usrDeselect = session['usrDeselect']
                order.remove_item(usrDeselect)
            except Exception as e:
                return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <script>alert(''' + str(e) + ''');</script>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a>Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a class="active">Select Food</a>
    <a> </a>
    <a> </a>
    <a>Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <h1 class="center">Select Food</h1>
  <br>
  <script>
    function addItems() {
    var content = document.getElementById("usrSelect");
    var selMenu = document.getElementById("selected-item-menu");
    selMenu.innerHTML = content.innerHTML + '<h5>''' + entry + '''</h5>';
    };

    function minItems() {
    var content = document.getElementById("usrSelect");
    var selMenu = document.getElementById("selected-item-menu");
    if (selMenu.innerHTML === " ") {
      alert("No items to remove.");
    }
    var selMenu.innerHTML = content.innerHTML - '<h5>''' + entry + '''</h5>';
    };
  </script>
  <div id="menu">
    <h3>Menu:</h3>
    ''' + str(laMenu['Name']) + '''
  </div>
  <div id="selected-item-menu">
    <h3>Selected items:</h3>
    ''' + str(usrSelect) + '''
  </div>
  <br>
    <h2>Add items to order:</h2>
    <form style="text-align:left;" id="sel" "action="addItems();" method="post">
      <div style="overflow: hidden; padding-right: .5em;">
        <input type="submit" value="Add" style="float: right" />
        <input type="text" style="width: 100%;" id="usrSelect" name="usrSelect" placeholder="Enter item code (code on the left of an item) to add to order"><br>
    </div>
  <br>
  <h2>Remove items from order:</h2>
  <form style="text-align:left;" id="sel2" "action="minItems();" method="post">
      <div style="overflow: hidden; padding-right: .5em;">
          <input type="submit" value="Remove" style="float: right" />
          <input type="text" style="width: 100%;" id="usrSelect" name="usrSelect" placeholder="Enter item code (code on the left of an item) to remove from order"><br>
      </div>
      <br>
      <br>
  </form>
</body>
</html>
'''
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a>Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a class="active">Select Food</a>
    <a> </a>
    <a> </a>
    <a>Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime()">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <h1 class="center">Select Food</h1>
  <br>
  <script>
    function addItems() {
    var content = document.getElementById("usrSelect");
    var selMenu = document.getElementById("selected-item-menu");
    
    selMenu.innerHTML = content.innerHTML + '<h5>''' + " " + '''</h5>';
    };

    function minItems() {
    var content = document.getElementById("usrSelect");
    var selMenu = document.getElementById("selected-item-menu");
    if (selMenu.innerHTML === " ") {
      alert("No items to remove.");
    }
    var selMenu.innerHTML = content.innerHTML - '<h5>''' + " " + '''</h5>';
    };
  </script>
  <div id="menu">
    <h3>Menu:</h3>
    ''' + str(laMenu) + '''
  </div>
  <div id="selected-item-menu">
    <h3>Selected items:</h3>
    ''' + str(usrSelect) + '''
  </div>
  <br>
  <h2>Add items to order:</h2>
  <form style="text-align:left;" id="sel" "action="addItems();" method="post">
      <div style="overflow: hidden; padding-right: .5em;">
          <input type="submit" value="Add" style="float: right" />
          <input type="text" style="width: 100%;" id="usrSelect" name="usrSelect" placeholder="Enter item code (code on the left of an item) to add to order"><br>
      </div>
  </form>
  <br>
  <h2>Remove items from order:</h2>
  <form style="text-align:left;" id="sel2" "action="minItems();" method="post">
      <div style="overflow: hidden; padding-right: .5em;">
          <input type="submit" value="Remove" style="float: right" />
          <input type="text" style="width: 100%;" id="usrSelect" name="usrSelect" placeholder="Enter item code (code on the left of an item) to remove from order"><br>
      </div>
  </form>
</body>
</html>
'''
    

@app.route('/order')
def order():
    if "Mozilla/5.0 (Nintendo WiiU) AppleWebKit" in request.headers.get('User-Agent'):
        if "NintendoBrowser" in request.headers.get('User-Agent'):
            print("[log]: someone tried to connect to the server on a wii u on the internet browser!")
            return "<script>alert('Access denied! Wii do not support the Internet Browser. Please access this on TVii instead. Sorry m8 :/');</script>"
        print("[log]: someone connected to the server on a wii u!")
    else:
        print("[log]: someone tried to connect to the server on a system that isn't a wii u!")
        # comment out line below for testing on pc
        return "<script>alert('Access denied! You are not on a Wii U system. This is not intended for use on a machine that is not a Wii U. Sorry m8 :/');</script>"
    
    return '''<!DOCTYPE html>
<html>
<head>
  <title>Macchiiato</title>
  <style>
    body {
      margin: 0;
      padding: 0px;
      position: relative;
      font-family: Nintendo_RodinNTLG-M;
      background-color: #e6e6e6;
      -webkit-overflow-scrolling:touch;
    }
    
    .center {
      text-align: center;
    }
    
    #bottom-tab {
      position: fixed;
      bottom: 0px;
      z-index: 3;
    }
  </style>
  <div class="topnav">
    <img id="mii-image" align="right" src="">
    <a>Address Info</a>
    <a> </a>
    <a> </a>
    <a>Set Name for Order</a>
    <a> </a>
    <a> </a>
    <a>Select Food</a>
    <a> </a>
    <a> </a>
    <a class="active">Order</a>
  </div>
  <script>
    const activeUserSlot = vino.act_getCurrentSlotNo();
    img = document.getElementById("mii-image");
    img.src=vino.act_getMiiImage(activeUserSlot);
  </script>
  <style>
  .topnav {
    background-color: #000;
    overflow: hidden;
  }

  .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 30px;
    text-decoration: none;
    font-size: 30px;
  }

  .topnav a.active {
    background-color: #0451AA;
    color: white;
  }
  </style>
</head>
<body onload="startTime();">
  <div class="navbuttons">
    <div id="header-exit"
    <="" div="">
    <img id="bottom-tab" src="''' + url_for('static',filename='bottom_tab.png') + '''"</img>
  <script>
    function startTime() {
      var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
      if( i < 10 ) {
        i = "0" + i;
      }
        return i;
      }

    if ( hour > 12 ) {
      hour = hour - 12;
      if ( hour == 12 ) {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";
      }
      else {
        hour = checkTime(hour);
      document.getElementById("tt").innerHTML = hour+":"+minute+" PM";
      }
    }
    else {
      document.getElementById("tt").innerHTML = hour+":"+minute+" AM";;
    }
    var time = setTimeout(startTime,1000);
    }
  </script>
  <table id="navstrings">
  <div id="today" style="font-size:14px; position: fixed; bottom: 26px; right: 62px; z-index: 5;"></div>
  <div id="tt" style="font-size:18px; position: fixed; bottom: 6px; right: 50px; z-index: 5;"></div>
  </table>
  <script>
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d = new Date();
    let day = weekday[d.getDay()];
    document.getElementById("today").innerHTML = day;
  </script>
  <h1 class="center">Order</h1>
  <br>
  <p class="center">Order page</p>
  <br>
  <a class="center" href="/menu"><p>Back</p></a>
</body>
</html>
'''

if True:
    app.run(host='0.0.0.0', port=8080)

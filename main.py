# letzter Stand

import shutil
from flask import Flask
from flask import render_template_string, redirect, request

import os
import subprocess
import socket

messages = []

app = Flask(__name__)

nav_bar = """                           <!--Navigationsleiste mit Formatierung-->
 <!DOCTYPE html>
    <html>
    <head>
        <title>Nachhilfemanager</title>
        <style>
            nav ul {                    <!--Anlegen des Menüs für Anwendungen-->
                list-style-type: none;  <!--Formatierung des Menüs-->
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #333;
            }

            nav li {
                float: left;            <!--Anordnung auf der linken Seite-->
            }

            nav li a {                  <!--Textformatierung-->
                display: block;
                color: white;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
            }
            nav li a:hover {
                background-color: #ddd;
                color: black;
            }
        </style>
    </head>
    <body>
        <h1>Nachhilfemanager 🏫</h1>
        <nav>                           <!--Anlegen der Links zu Anwendungen-->
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/kontakte">Kontakte</a></li>
                <li><a href="/dateien">Dateien</a></li>
                <li><a href="/forum">Forum</a></li>
            </ul>
        </nav>
    </body>
    </html>
"""

@app.route('/')                          <!--Methode zum Aufrufen des Home-Bildschirms-->
def home():
    return render_template_string(nav_bar)

@app.route('/kontakte')                  <!--Methode zum Aufrufen der Kontakte-->
def kontakte():
    return render_template_string(nav_bar + """

    <h3>Lehrer</h3>

<table>                                  <!--Tabelle mit Lehrern ubnd Fächern-->
  <tr>
    <th>Herr ... </th>
    <th>Herr ... </th>
    <th>Frau ... </th>

    
  </tr>
  <tr>
    <td>Deutsch </td>
    <td>Mathematik </td>
    <td>Französisch </td>
   </tr>
   <tr>
     <td>Argumentieren </td>
     <td>Stochastik </td>
     <td>Passé Composé</td>
   </tr>
</table>
    </html>
    """)


@app.route('/dateien')                  <!--Methode zum Aufrufen der Dateien-->
def root():
    return render_template_string(nav_bar + '''
        <html>                          <!--Aufrufen der versch. Dateien oder Verzeichnisse-->
          <head>
            <h3>Lernmaterialien</h3>
          </head>
          <body>
           <p align = "center"> <Strong> Aktuelles Verzeichnis:</Strong> {{show_current_path}}</p>
           <ul>
           {% for item in file_list %}
              {% if "." not in item%}
               <li><strong><a href="/cd?path={{current_path + '/' + item}}">{{item}}</a></strong> </li>
              {% elif '.txt' or  '.json' or '.html' in item %}
              <li><strong><a href = "/view?file={{current_path + '/' + item +'.txt'}}">{{item}}</a></strong></li>
              {% else %}
              <li>{{item}}</li>
              {%endif%}
           {%endfor%}
          </body>
        </html>
    ''', show_current_path = os.getcwd().replace('/Users/jonas/PycharmProjects/Nachhilfe Manager', '/'),
        current_path = os.getcwd(),

         file_list = subprocess.check_output('ls', shell=True, cwd= os.getcwd()).decode('utf8').split('\n',))

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        message = request.form['message']
        messages.append(message)

        return render_template_string(nav_bar + """
        <h3> Forum </h3>
        <form action="/forum" method="post">
        <div align="left" style="width: px; height: 300px; overflow-y: auto; border: 1px solid #ccc;">
         <div>
          {% for message in messages %}
           <p>&nbspAbsenderName: {{ message }}</p><br></br>
        {% endfor %}
          </div>
         </div>
         <p><label>Stelle eine Frage:</label></p>
          <textarea id="message" name="message" rows="4" cols="50"></textarea>
          <br>
          <input type="submit" value="Senden ✉️">
        </form>
        </body>
        </html>
        """, message=message,
             messages=messages)
    else:
        return render_template_string(nav_bar + """
        <h3> Forum </h3>
        <form action="/forum" method="post">
        <div align="left" style="width: px; height: 300px; overflow-y: auto; border: 1px solid #ccc;">
         <div>
          {% for message in messages %}
           <p>&nbspAbsenderName: {{ message }}</p><br></br>
          {% endfor %}
          </div>
         </div>
         <p><label>Stelle eine Frage:</label></p>
          <textarea id="message" name="message" rows="4" cols="50"></textarea>
          <br>
          <input type="submit" value="Senden ✉️">
        </form>
        </body>
        </html>
        """)


@app.route('/cd')
def cd():
    os.chdir(request.args.get('path'))
    return redirect('/')

@app.route('/view')
def view():
    return subprocess.check_output('cat ' + request.args.get('file'), shell=True).decode('utf-8').replace('n', '<br>')
# nur für eingeloggte nutzer


# später zu socket server wechseln

if __name__ == '__main__':
    app.run(debug=True, port=3000)

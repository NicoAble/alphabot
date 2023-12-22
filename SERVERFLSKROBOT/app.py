import Alphabot
import time
import sqlite3
import hashlib
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

def MandaComandi(comando):
    lista_comandi = []
    con=sqlite3.connect("comandi.db")
    res1=con.execute("SELECT shortcut_name FROM tabellaMovements")
    list=res1.fetchall()
    for i, element in enumerate(list):
        list[i]= element[0]
    print(f"lista comandi = {list}")
    print(f"comando = {comando}")
    if(comando in list):
        res=con.execute(f"SELECT movement_sequence FROM tabellaMovements WHERE UPPER(shortcut_name) = UPPER('{comando}')")
        #print(f"risultato query {res.fetchall()}")
        lista_comandi=str(res.fetchall()[0][0]).split("/")#ritorna lista con tutti i risultati
    else: print("comando non in lista")
    print(f"comandi ricevuti= {lista_comandi}")
    con.close()
    return lista_comandi


def controllaComando(com, Ab):
    comando=com.split(";")
    ciclo = 0
    if(len(comando[0])>=1):
        #print("verso la funzione")
        lista_comandi=MandaComandi(comando[0])
        ciclo=len(lista_comandi)
        #print(f"lista comandi: {lista_comandi}")
    else: 
        ciclo = 1
        
    if(ciclo <= 0): ciclo=1

    print(ciclo)
    i=0
    for i in range(0, ciclo):
        print("ciclo")
        if(ciclo >= 1):
            t=lista_comandi[i]
        print(t)
        l=t.split(',')
        t=l[0]
        pwm=l[1]
        pwm=float(pwm)
        if pwm < 27: pwm=27
        elif pwm > 100: pwm=100
        i=float(t[2:])
        if(t[1]==";"):
            if((t[:1]=='F') or t[:1]=='f'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    Ab.forward()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: print(b"error") #questo address è quello del client che ha mandato dati al server
            elif((t[:1]=='B') or t[:1]=='b'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    Ab.backward()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: print(b"error") 
            elif((t[:1]=='L') or t[:1]=='l'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    Ab.left()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: print(b"error") 
            elif((t[:1]=='R') or t[:1]=='r'):
                if(i>0):
                    Ab.set_pwm_a(pwm)
                    Ab.set_pwm_b(pwm)
                    Ab.right()
                    time.sleep(i)        #durata del movimento
                    Ab.stop()
                else: print(b"error") 
            elif((t[:1]=='E') or t[:1]=='e'):
                print(b"exit") 
                print("esecuzione terminata forzatamente")
                break
            else: print(b"error") 
        else: print(b"error")


def validate(username, password):
    completion = False
    con = sqlite3.connect('psw_db.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM UTENTI;")
    rows = cur.fetchall()
    for row in rows:
        print (row)
        dbUser = row[0]
        dbPass = row[1]
        print(dbPass)
        print(dbUser)
        print(username)
        print(password)
        print(hashlib.sha256(password.encode('utf-8')).hexdigest())
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    user_password=hashlib.sha256(user_password.encode('utf-8')).hexdigest()
    return hashed_password == user_password


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route("/secret", methods=['GET', 'POST'])
def index():
    Ab=Alphabot.AlphaBot() 
    i = 0.7
    if request.method == 'POST':
        comando = request.form['comando']
        
        #print(request.form.get('action1'))
        if request.form.get('action1') == 'avanti':
            #print("Bottone1")
            Ab.forward()
            time.sleep(i)        #durata del movimento
            Ab.stop()
        elif  request.form.get('action2') == 'indietro':
            #print("Bottone2")
            
            Ab.backward()
            time.sleep(i)        #durata del movimento
            Ab.stop()
            
        elif  request.form.get('action3') == 'destra':
            #print("Bottone3")
            i += 0.35
            Ab.right()
            time.sleep(i)        #durata del movimento
            Ab.stop()
            i = 0.7
        elif  request.form.get('action4') == 'sinistra':
            #print("Bottone4")
            i += 0.45
            Ab.left()
            time.sleep(i)        #durata del movimento
            Ab.stop()
            i = 0.7
        else: 
            controllaComando(comando, Ab)
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    print("ciao")
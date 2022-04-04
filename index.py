from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

# Update connection string information
conn = psycopg2.connect(database="testdb", user="admin", password="890819", host="127.0.0.1", port="5432")
cursor = conn.cursor()


# @app.route("/")
# def index():
#     db.create_all()
#     return "資料成功連接"


@app.route('/insert')
def insert():
       sql = "INSERT INTO students (name, tel, addr, email) VALUES ('dafsa','zssss4', 'saddd', 'dsadaa');"
       cursor.execute(sql)
       conn.commit()
       return 'DATA HAS SAVED'


@app.route('/queryall')
def queryall():
        sql = """ SELECT * FROM students """     
        cursor.execute(sql)
        conn.commit()
        row = cursor.fetchone()
        conn.close()
        return render_template('test.html', row=row)


@app.route('/api/testing/<string:name>')
def testing(name):
        now = datetime.now()
        return render_template('test.html', **locals())

@app.route("/api/login", methods=['GET', 'POST'])
def login():   
    if request.method == "POST":
        username = request.values['username']
        password = request.values['password']
        if username == 'fiona' and password == "123456":
            return 'hello'
        else:
            return 'username or password is false'    


    return '''
    <form method="post" action='/api/login'>
    <p> username:<input type="text" name="username"></input> </p>
    <p> password:<input type="text" name="password"></input> </p>
    <button type="submit"> submit </button>
    </form>
    '''

if __name__ == "__main__":
    app.run()  

    
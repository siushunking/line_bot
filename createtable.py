from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:890819@127.0.0.1:5432/NSYSU_QUESTION'
db = SQLAlchemy(app)

@app.route('/')
def index():
    sql = """
    CREATE TABLE qna (
    id serial NOT NULL,
    uid character varying(50) NOT NULL,
    question character varying(250) NOT NULL,
    PRIMARY KEY (id))
    """
    db.engine.execute(sql)
    return "資料表建立成功！"

if __name__ == '__main__':
   app.run(debug=True)
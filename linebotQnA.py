from flask import Flask

app = Flask(__name__)
from flask import request, abort
from flask_sqlalchemy import SQLAlchemy
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import http.client, json

line_bot_api = LineBotApi('Line(channel_access_token)')
handler = WebhookHandler('Line(Channel secret)')

#pip install line-bot-sdk 先安裝此程式

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']  # get X-Line-Signature header value #若不明的可以先理解為連接line
    body = request.get_data(as_text=True)   # get request body as text #即刻使用者輸入內容
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:  #若api token錯誤 ，連接會失敗
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

#AZURE 連接
host = 'AZURE(host)'  
endpoint_key = 'AZURE_endpoint_keY'  
kb = 'AZURE_KB'
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"

#db連接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:890819@127.0.0.1:5432/NSYSU_QUESTION'
db = SQLAlchemy(app)



@handler.add(MessageEvent, message=TextMessage) # 意見是當有message 要執行的event
def handle_message(event):  
    infoText = event.message.text
    if infoText == '如何使用':
        sendInfoUser(event)
    else:
        sendQnA(event, infoText)

def sendInfoUser(event):  #使用說明
    try:
        text1 ='''
        這是關於中山大學選課的資料，
        請輸入關於中山大學選課的相關問題。
               '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message) #當收到如何使用時的動作
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))




def sendQnA(event, infoText):  #QnA  參數是 接收event 和 infotext是收到message內容
    question = {
        'question': infoText,
    }
    content = json.dumps(question) #將受到json 變成python 可以看到內容
    #azure 連線 
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }

    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", method, content, headers)
    response = conn.getresponse ()
    result = json.loads(response.read())
    print(result)
    result1 = result['answers'][0]['answer']
    print(result1)

    if 'No good match' in result1:
        text1 = '很抱歉，資料庫中無適當解答！\n請再輸入問題,我們會改進我們ai客服'
        #將沒有解答的問題寫入資料庫
        
        userid = event.source.user_id #line user_id
        sql_cmd = "insert into qna (uid, question) values('" + userid + "', '" + infoText +"');"
        db.engine.execute(sql_cmd)
        message = TextSendMessage(
        text = text1
    )
        line_bot_api.reply_message(event.reply_token,message)
    else:
        result2 = result1[1:]  #移除「A：」
        text1 = result2  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token,message)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

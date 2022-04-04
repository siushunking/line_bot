# line_chatbot
## 系統簡介

使用者可透過聊天機器人獲得資訊或解決問題。聊天機器人會搭載自然語言處理系統，系統不是透過擷取輸入的關鍵字，而是透過自然語言處理
系統處理資訊，再從語料庫（QnAMarker)中找尋最合適的應答句。 若果資料庫沒有相關答案， 系統會儲存有關data， 以作之後 更好訓練

聊天機器人是虛擬助理，可以幫助使用者進行娛樂目的的聊天室，研究和特定產品促銷，社交機器人等。
此次以中山大學選課常見問題，建立ai聊天機器人。（純粹練習AIline_bot，非官方智慧客服）🫣
### 可以看見 客服懂得回覆使用者
![WhatsApp Image 2022-04-04 at 4 56 24 AM](https://user-images.githubusercontent.com/85872659/161448313-e67b0fb9-8e7b-4d03-a883-05fbb47f242b.jpeg)

### 可以看見 因為資料庫沒有猴子訓練，因此會將資料傳入data，以作之後 更好訓練，同時建立 database
```
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
```

<img width="495" alt="螢幕截圖 2022-04-04 上午5 14 13" src="https://user-images.githubusercontent.com/85872659/161448934-fda2df72-dc9b-43cf-bc14-e4d20fd3bb42.png">

## 開始操作

若果使用macbook 有可能出現[SSL: CERTIFICATE_VERIFY_FAILED]，因此你要在python folder 雙擊Install Certificates.command
<img width="1016" alt="螢幕截圖 2022-04-04 上午12 11 43" src="https://user-images.githubusercontent.com/85872659/161437266-b607e251-c14c-4420-8c81-8a2fe7476ef3.png">
<img width="688" alt="螢幕截圖 2022-04-04 上午12 14 17" src="https://user-images.githubusercontent.com/85872659/161437387-139c949f-bb32-4286-8747-dccccfa55de8.png">



前期作業 請參考以下影片。
How to get started with Azure QnA Maker and publish a bot quickly | [Azure Developer Streams](https://www.youtube.com/watch?v=sxy9ZTC3BhA)
1. 在azure建立資源
2. QNA marker中提交問題和答案， AZURE會自行處理有關自然語言處理，機器學習。 


連接api 請參考以下
更多資料請參考官方document [Azure-Samples](https://github.com/Azure-Samples/cognitive-services-qnamaker-python/blob/master/documentation-samples/quickstarts/get-answer/get-answer-3x.py)


// Represents the various elements used to create HTTP request URIs
  // for QnA Maker operations.
  // From Publish Page
  // Example: YOUR-RESOURCE-NAME.azurewebsites.net
  // CAUTION: This is not the exact value of HOST field
  // HOST trimmed to work with http library
  host = "YOUR-RESOURCE-NAME.azurewebsites.net";

  // Authorization endpoint key
  // From Publish Page
  endpoint_key = "YOUR-ENDPOINT-KEY";

   //Management APIs postpend the version to the route
   //From Publish Page
   //Example: /knowledgebases/ZZZ15f8c-d01b-4698-a2de-85b0dbf3358c/generateAnswer
   //CAUTION: This is not the exact value after POST
   //art of HOST is prepended to route to work with http library
  route = "/qnamaker/knowledgebases/e7015f8c-d01b-4698-a2de-85b0dbf3358c/generateAnswer";
  
```  
headers = {
    'Authorization': 'EndpointKey ' + endpoint_key,
    'Content-Type': 'application/json'
}

try:
  conn = http.client.HTTPSConnection(host,port=443)

  conn.request ("POST", route,  question, headers)

  response = conn.getresponse ()

  answer = response.read ()

  print(json.dumps(json.loads(answer), indent=4))

except :
    print ("Unexpected error:", sys.exc_info()[0])
    print ("Unexpected error:", sys.exc_info()[1])
```


建立一個內網但不使用ip address，而是ngrok
1. 在ngrok建立內網何服器，安裝ngrok.exe。
2. 然後 在終端機cd到ngrok.exe位置 eg在desktop ， 在終端機 輸入cd desktop
3. mac 在終端輸入 ./ngrok http 5000. window: ngrok http 5000 (埠碼根據你程式而定)

4. 然後在messaging api 給line webhook url，就是在 ngrok 分配到網址 
<img width="687" alt="螢幕截圖 2022-04-03 上午1 49 26" src="https://user-images.githubusercontent.com/85872659/161395121-71e50aef-6431-4020-a1fc-5d4d3bd27027.png">


5. 因為程式路徑是/callback。所以記得line webhook url是{{ngrok_url/callback}}，而非單單ngrok_url

6. 最後建立line的 api 程式部分， 內容請參考以下api。 
 [line api 連接](https://github.com/line/line-bot-sdk-python)
 ```
 from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
 ```

7. 就可以用程式建立人工客服與使用者互動啦！
![WhatsApp Image 2022-04-04 at 4 56 24 AM](ht

import os
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
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

app = Flask(__name__)

# LINE bot 的 Channel access token 和 Channel secret
# 請將 YOUR_CHANNEL_ACCESS_TOKEN 和 YOUR_CHANNEL_SECRET 替換為你的 LINE bot 設定值
channel_secret = os.getenv('ChannelSecret', None)
channel_access_token = os.getenv('ChannelAccessToken', None)
line_bot_api = LineBotApi(ChannelAccessToken)
handler = WebhookHandler(ChannelSecret)

# agent builder 設定
project_id = os.getenv('ProjectId', None)  # 你的 Google Cloud 專案 ID
location = os.getenv('Loaction', None)  # 資料庫位置，例如： "global", "us", "eu"
engine_id = os.getenv('EngineId', None)  # 你的搜尋引擎 ID

def answer_query_sample(
    project_id: str,
    location: str,
    engine_id: str,
    query: str,
):
    """
    使用指定的搜尋引擎回答查詢。
    """
    # 設定客戶端選項，指定 API 端點
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # 建立對話式搜尋客戶端
    client = discoveryengine.ConversationalSearchServiceClient(client_options=client_options)

    # 完整的 serving config 資源名稱
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_serving_config"

    # 查詢理解規格（目前為空，可以根據需求設定）
    query_understanding_spec = discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec()

    # 答案生成規格，設定回應語言為繁體中文
    answer_generation_spec = discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
        answer_language_code="zh-TW",
        ignore_adversarial_query=False,  # Optional: Ignore adversarial query
        ignore_non_answer_seeking_query=False,  # Optional: Ignore non-answer seeking query
        ignore_low_relevant_content=False,  # Optional: Return fallback answer when content is not relevant
        model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
            model_version="gemini-1.5-flash-002/answer_gen/v1",  # 使用 Gemini 1.5 flash 模型
        ),
        prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
            preamble="你是一個旅遊網站的 AI 助手，名字叫做可樂，你的任務是根據使用者的搜尋結果，產生更具體且吸引人的說明文字，以提升點擊率。將用戶給予的輸入文字截取實體，依據實體回答，給定一個用戶和可樂之間的對話以及一些搜尋結果，為妳創建一個最終答案。答案應使用搜尋結果中的所有相關信息，不引入任何額外信息，並盡可能使用與搜尋結果完全相同的詞。妳的答案不應超過 800字元數，儘量使用條列式並整理成易讀編排回答，關於價錢只要回覆有近似值的答案。使用使用者的問題語系回答。回答中相同行程的URL，只需要出現在最開頭。不使用markdown語法。找不到相關資訊時，請統一回覆請輸入更詳細資訊",  # Optional: Natural language instructions for customizing the answer.
        ),
        include_citations=True,  # Optional: Include citations in the response
    )

    # 建立答案查詢請求
    request = discoveryengine.AnswerQueryRequest(
        serving_config=serving_config,
        query=discoveryengine.Query(text=query),
        session=None,  # 設定為 None 表示新的對話
        query_understanding_spec=query_understanding_spec,
        answer_generation_spec=answer_generation_spec,
    )

    # 發送請求並取得回應
    response = client.answer_query(request)
    # print(response) #印出完整回覆，方便debug

    return response

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
    # 取得使用者傳來的訊息
    user_message = event.message.text
    print(user_message)

    # 使用 Discovery Engine 回答查詢
    response = answer_query_sample(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
        query=user_message,
    )

    #line_ans = response.answer.answer_text
    line_ans = f"""{response.answer.answer_text}
以下是相關網址：

* {response.answer.steps[0].actions[0].observation.search_results[0].title}
  {response.answer.steps[0].actions[0].observation.search_results[0].uri}

* {response.answer.steps[0].actions[0].observation.search_results[1].title}
  {response.answer.steps[0].actions[0].observation.search_results[1].uri}

* {response.answer.steps[0].actions[0].observation.search_results[2].title}
  {response.answer.steps[0].actions[0].observation.search_results[2].uri}
    """
    
    # 回覆使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=line_ans)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)
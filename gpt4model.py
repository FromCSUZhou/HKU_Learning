import openai
import streamlit as st
import pymongo
import requests
import json

# Step 1: Obtain OpenAI API key
api_keys = st.secrets["API_KEYS"]
# user_keys = st.secrets["USER_KEYS"]
# mongo_url = st.secrets["MONGO_URL"]
MONGO_URL_findOne = st.secrets["MONGO_URL_findOne"]
MONGO_URL_updateOne = st.secrets["MONGO_URL_updateOne"]
MONGO_KEY = st.secrets["MONGO_KEY"]

def find_one(user_key):
    payload = json.dumps({
        "collection": "email_info",
        "database": "email_monitoring_db",
        "dataSource": "ChatgptUsing",
        "filter": {"email_address": user_key},
    })
    headers = {
                  'Content-Type': 'application/json',
                  'Access-Control-Request-Headers': '*',
                  'api-key': MONGO_KEY,
    }
    response = requests.request("POST", MONGO_URL_findOne, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)

def update_one(user_key, new_count):
    payload = json.dumps({
        "collection": "email_info",
        "database": "email_monitoring_db",
        "dataSource": "ChatgptUsing",
        "filter": {"email_address": user_key},
        "update": {
         "$set": { "count":  new_count }
     }
    })
    headers = {
                  'Content-Type': 'application/json',
                  'Access-Control-Request-Headers': '*',
                  'api-key': MONGO_KEY,
    }
    response = requests.request("POST", MONGO_URL_updateOne, headers=headers, data=payload)
    print(response.text)
# def create_mongo_connection():
#     # 用你的 MongoDB 服务器地址和端口替换 'mongodb://localhost:27017'
#     mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
#     db = mongo_client['email_monitoring_db']
#     collection = db['email_info']
#     return collection

def generate_result(prompt, model):
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            # temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        message = completion.choices[0].message.content
    except Exception as e:
        message = "网络出错啦，刷新后再试一下吧~"
        print(e)
    return message



def main():
    # st.set_page_config(page_title="单词故事", page_icon=":robot:", layout="wide")
    st.title("Super Power GPT-4")
    # st.markdown("**pg群内部专属**")
    user_key = st.text_input("输入你的邮箱 Input your activation email", key="user_key_ielts")
    input_words = st.text_area("请输入问题(问题越详细越好哦～):", key="question_input")
    st.markdown("增加GPT-4模型使用次数:https://bvcbon59znit5rct.mikecrm.com/LRrfYaY")
    # st.markdown("意见/建议以及各种需求欢迎反馈到邮箱：englishtool@hotmail.com")
    # st.markdown("意见/建议以及各种需求欢迎反馈到邮箱：gptplus@163.com")

    prompt = input_words

    # model = "text-davinci-003"
    model = "gpt-4-0314"
    # temperature = 1
    # max_tokens = 2000
    max_input_len = 8000

    if st.button("确认", key="word_gpt4"):
        email_data = find_one(user_key)
        if email_data["document"]:
            new_count = email_data["document"]["count"] - 1
            if new_count >= 0:
                if input_words.__len__() < max_input_len:
                    with st.spinner('答案生成中...'):
                        result = generate_result(prompt, model)
                        if result != "网络出错啦，刷新后再试一下吧~":
                            st.balloons()
                            st.success("大功告成！")
                            update_one(user_key, new_count)
                            st.markdown(f"剩余次数：{new_count}")
                            st.markdown(result)
                        else:
                            st.markdown(result)
                            st.markdown("本次不会消耗您的使用次数，请刷新之后再试或者联系管理员～")
                        print(f"\ninput:\n{input_words}\noutput:\n{result}\n\n")
            else:
                st.info("次数用完啦~")
        else:
            st.info("邮箱不正确~")



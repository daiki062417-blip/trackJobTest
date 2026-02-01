import streamlit as st

data = []   #評価データを保存する

contentValue = st.slider(
    'タスクの内容に関する評価', 0, 10, key='content'
)
personValue = st.slider(
    '引継ぎ相手に関する評価', 0, 10, key='person'
)
scheduleValue = st.slider(
    'スケジュールに関する評価', 0, 10, key='schedule'
)

st.write("content:", contentValue)
st.write("person:", personValue)
st.write("schedule:", scheduleValue)

data.append([contentValue, personValue, scheduleValue]) #評価データ作成


with open("sample.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(data)

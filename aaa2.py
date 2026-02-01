import streamlit as st
import pandas as pd
import os

#登録タスクの表示
if os.path.isfile("tasks.csv"):

        #人名
        name = st.text_input("名前")

        #ファイル読み込み
        df = pd.read_csv("tasks.csv")

        #全タスクの評価を保存する配列
        #0: タスク評価, 1: 相手評価, 2: スケジュール評価
        dataList = [[]] 

        #全タスクの評価欄を表示
        for i in range(len(df)):

            #タスク表示
            st.write("タスク名: " +str( df.loc[i, "タスク名"]) ) 
            st.write("タスクの詳細: " + str( df.loc[i, "タスクの詳細"] ) )
            st.write("タスクを行う時期・日時: " + str( df.loc[i, "タスクを行う時期・日時"] ) )
            st.write("引き継ぎ担当者: " +str(  df.loc[i, "引き継ぎ担当者"] ) )

            #提出フォーム
            with st.form(key='evaluate_form' + str(i)):

                #スライダーで10段階評価する
                contentValue = st.slider(
                    'タスクの内容に関する評価', 0, 10, key='content'+str(i)
                )
                personValue = st.slider(
                    '引継ぎ相手に関する評価', 0, 10, key='person'+str(i)
                )
                scheduleValue = st.slider(
                    'スケジュールに関する評価', 0, 10, key='schedule'+str(i)
                )

                #提出ボタン
                submitted = st.form_submit_button("提出")

                #保存処理
                if submitted:
                    if contentValue * personValue * scheduleValue != 0:
                        
                        #成功表示
                        st.success("評価が完了しました。")
                        st.balloons()
                        
                        #評価データ
                        data2 = pd.DataFrame(
                                [[name, str( df.loc[i, "タスク名"]), contentValue, personValue, scheduleValue]], 
                                columns=["人名","タスク名","タスクの内容に関する10段階評価","引き継ぎ相手に関する10段階評価", "スケジュールに関する評価"]
                            )  

                        #csvにデータを書き込み
                        DATA_FILE2 = "tasks2.csv"

                        if not os.path.isfile(DATA_FILE2):
                            data2.to_csv(DATA_FILE2, index=False, encoding='utf-8-sig')
                        else:
                            data2.to_csv(DATA_FILE2, mode='a', header=False, index=False, encoding='utf-8-sig')
                    
                    #評価していない項目があれば警告
                    else:
                        st.error("全評価を1~10段階で行ってください。")
            

elif st.session_state.page == 'application':
    st.title("🙋 引き継ぎ希望申請")
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()
    
    st.title("引継ぎ希望申請")

    #登録タスクの表示
    if os.path.isfile("tasks.csv"):

            #ファイル読み込み
            df = pd.read_csv("tasks.csv")

            st.write("タスク名: " +str( df.loc[0, "タスク名"]) ) 
            st.write("タスクの詳細: " + str( df.loc[0, "タスクの詳細"] ) )
            st.write("タスクを行う時期・日時: " + str( df.loc[0, "タスクを行う時期・日時"] ) )
            st.write("引き継ぎ担当者: " +str(  df.loc[0, "引き継ぎ担当者"] ) )
                

    with st.form(key='evaluate_form'):

        #スライダーで10段階評価する
        contentValue = st.slider(
            'タスクの内容に関する評価', 0, 10, key='content'
        )
        personValue = st.slider(
            '引継ぎ相手に関する評価', 0, 10, key='person'
        )
        scheduleValue = st.slider(
            'スケジュールに関する評価', 0, 10, key='schedule'
        )

        #提出ボタン
        submitted = st.form_submit_button("提出")

        #保存処理
        if submitted:
            if contentValue * personValue * scheduleValue != 0:
                #csvにデータを書き込み
                DATA_FILE2 = "tasks2.csv"

                #評価データ
                if os.path.isfile("tasks2.csv"):
                    personIndex = len(pd.read_csv("tasks2.csv"))
                else :
                    personIndex = 1
                data2 = pd.DataFrame(
                        [["匿名"+str(personIndex), contentValue, personValue, scheduleValue]], 
                        columns=["評価者","内容評価値","人評価値", "日程評価値"]
                    )  

                if not os.path.isfile(DATA_FILE2):
                    data2.to_csv(DATA_FILE2, index=False, encoding='utf-8-sig')
                else:
                    data2.to_csv(DATA_FILE2, mode='a', header=False, index=False, encoding='utf-8-sig')

                 #成功表示
                st.success("評価が完了しました。")
                st.balloons()
     
            #評価していない項目があれば警告
            else:
                st.error("全評価を1~10段階で行ってください。")

import streamlit as st
import pandas as pd
import os
import itertools

#先にモデルを組む
def solve_matching(app_df, tasks_df):
    w1, w2, w3 = 0.5, 3.0, 1.0

    valid_candidates = []
    for _, row in app_df.iterrows():
        t_eval = row['タスクの内容に関する10段階評価']
        p_eval = row['引き継ぎ相手に関する10段階評価']
        s_eval = row['スケジュールに関する評価']
        
        # あなたが指定した「足切り条件」
        if t_eval <= 3 or p_eval <= 4 or s_eval <= 3:
            continue
            
        score = (t_eval * w1) + (p_eval * w2) + (s_eval * w3)
        valid_candidates.append({
            'name': row['人名'],
            'task': row['タスク名'],
            'score': score
        })
    
    all_tasks = df1['タスク名'].unique()
    all_people = df2['人名'].unique()
    
    best_total_score = -1
    best_combination = []

    for combination in itertools.permutations(all_people, len(all_tasks)):
        current_total_score = 0
        current_pairing = []
        is_valid_combo = True

        for i, task_name in enumerate(all_tasks):
            person_name = combination[i]
            # この人がそのタスクに対して有効な(足切りされていない)データを持っているか確認
            match = next((c for c in valid_candidates if c['name'] == person_name and c['task'] == task_name), None)
            
            if match:
                current_total_score += match['score']
                current_pairing.append({"タスク名": task_name, "担当者": person_name, "個人スコア": round(match['score'], 2)})
            else:
                is_valid_combo = False
                break
        
        if is_valid_combo and current_total_score > best_total_score:
            best_total_score = current_total_score
            best_combination = current_pairing
    return best_combination, best_total_score


# 1. ページの設定
st.set_page_config(page_title="引き継ぎ管理アプリ", page_icon="📝")

# 2. デザイン（CSS）
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    div.stButton > button {
        border-radius: 12px;
        border: 2px solid #6cace4;
        background-color: white;
        color: #6cace4;
        font-weight: bold;
        transition: 0.2s;
        width: 100%;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        background-color: #6cace4;
        color: white;
    }
    .stForm {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 状態管理とナビゲーション
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def navigate_to(page_name):
    st.session_state.page = page_name

# --- ホーム画面 ---
if st.session_state.page == 'main':
    st.title("✨ 引き継ぎ管理アプリ ✨")
    st.write("自分が行いたい業務を選んでください")
    st.divider() 

    
    if st.button("📥 タスク入力"):
        navigate_to('task_input')
    if st.button("📋 タスク一覧"):
        navigate_to('task_list')
    if st.button("🙋 引き継ぎ希望申請"):
        navigate_to('application')
    if st.button('🧹 最適な引き継ぎ先の確認・情報リセット'):
        navigate_to('results_reset')

# --- 「タスク入力」画面 ---
elif st.session_state.page == 'task_input':
    st.title("📥 タスク入力")
    
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun() 
    
    with st.form(key='task_form'):
        # 重複していた入力フィールドを統合
        task_name = st.text_input("📋 タスク名", placeholder="例：議事録の作成")
        task_detail = st.text_area("📝 タスクの詳細")
        task_date = st.text_input("📅 タスクを行う時期・日時") 
        task_assignee = st.text_input("👤 引き継ぎ担当者")
        
        submitted = st.form_submit_button("提出")

        if submitted:
            # 1. まずデータを保存する
            data = pd.DataFrame(
                [[task_name, task_detail, task_date, task_assignee]], 
                columns=["タスク名", "タスクの詳細", "タスクを行う時期・日時", "引き継ぎ担当者"]
            )
            DATA_FILE = "tasks.csv"

            if not os.path.isfile(DATA_FILE):
                data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            else:
                data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

            # 2. 演出と完了通知
            st.balloons()
            st.success("タスクが正常に保存されました")
            
            # 3. 最後に画面を切り替える
            navigate_to('main')
            st.rerun()
    
# --- 「タスク一覧」画面 ---
elif st.session_state.page == 'task_list':
    st.title("📋 タスク一覧")
    
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()

    if os.path.isfile("tasks.csv"):
        df1 = pd.read_csv("tasks.csv")
        st.dataframe(df1,use_container_width=True )
        st.info(f"現在、{len(df1)}件のタスクが登録されています。")
    else:
        st.warning("まだ登録されたタスクはありません")

    
#「引き継ぎ希望申請」の画面
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
    


#『最適な引き継ぎ先の確認・情報リセット」の画面
#画面部分のコード
elif st.session_state.page == 'results_reset':
    st.title("最適な引き継ぎ先の確認・情報リセット")

    if st.button("🏠 ホームに戻る"):
        st.session_state.page = 'main'
        st.rerun()

    if os.path.isfile("tasks.csv") and os.path.isfile("tasks2.csv"):
        df1 = pd.read_csv("tasks.csv")
        df2 = pd.read_csv("tasks2.csv")

        st.subheader("最適な引き継ぎ先一覧")

        best_pairing, total_score = solve_matching(df2, df1)
        if best_pairing:
            st.success(f"全体の合計スコアが最大（{round(total_score, 2)}点）になる組み合わせを算出しました！")
            result_df = pd.DataFrame(best_pairing)
            st.table(result_df)
        
        else:
            st.warning("条件を満たす組み合わせが見つかりませんでした。評価を緩めるか、回答を増やしてください。")

    else:
        st.error("データが見つかりません。")
        
    if st.button("データのリセット"):
        if os.path.exists("tasks.csv"): os.remove("tasks.csv")
        if os.path.exists("tasks2.csv"): os.remove("tasks2.csv")
        st.warning("全てのデータを削除しました。")
        st.rerun()

    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()


# --- 「引き継ぎ希望申請」画面 ---
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


        navigate_to('main')
        st.rerun()
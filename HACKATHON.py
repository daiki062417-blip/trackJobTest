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
    
    all_tasks = tasks_df['タスク名'].unique()
    all_people = app_df['人名'].unique()
    
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
st.set_page_config(
    page_title="引き継ぎ管理アプリ", 
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. デザイン（CSS）- 極簡潔・ミニマルスタイル
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500&display=swap');
    
    .stApp { 
        background-color: #ffffff;
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    /* コンテナの幅を少し狭めて中央に寄せる */
    .main .block-container {
        max-width: 600px;
        padding-top: 5rem;
    }

    /* タイトル：装飾を消してシンプルに */
    h1 {
        text-align: center;
        color: #333;
        font-size: 1.8rem;
        margin-bottom: 2rem;
    }

    /* ボタンのスタイル：フラットでシンプルな横長 */
    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #eee;
        background-color: #fafafa;
        color: #444;
        width: 100%;
        height: 55px !important; /* 押しやすい適度な高さ */
        margin-bottom: 12px;
        font-size: 16px;
        transition: all 0.2s ease;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important; /* 左寄せ */
        padding-left: 25px !important;
    }

    /* ホバー：色は変えず、影と境界線だけで「押せる感」を出す */
    div.stButton > button:hover {
        border-color: #bbb;
        background-color: #f0f0f0;
        color: #000;
        transform: none; /* 浮かび上がらせない */
    }

    /* アイコン（絵文字）のサイズ調整 */
    div.stButton > button p {
        font-size: 1.2rem !important;
        margin-right: 15px !important;
        margin-top: 0 !important;
    }
            
    /* タブレット・スマホ（768px以下）向けの微調整 */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 2rem; /* 上下の余白を少し詰める */
    }
    div.stButton > button {
        height: 50px !important;
        font-size: 15px; /* 文字サイズをスマホ最適化 */
        padding-left: 15px !important; /* 左の余白を少し詰める */
    }
}
    </style>
    """, unsafe_allow_html=True)

# 3. 状態管理とナビゲーション
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def navigate_to(page_name):
    st.session_state.page = page_name

# --- ホーム画面（リスト形式） ---
if st.session_state.page == 'main':
    st.markdown("<h1>引き継ぎ管理システム</h1>", unsafe_allow_html=True)
    
    # 縦一列にシンプルに配置
    if st.button("📥タスクを入力する"):
        navigate_to('task_input')
        st.rerun()
        
    if st.button("📋タスク一覧を確認する"):
        navigate_to('task_list')
        st.rerun()
        
    if st.button("🙋引き継ぎ希望を申請する"):
        navigate_to('application')
        st.rerun()
        
    if st.button("🧹マッチング結果・リセット"):
        navigate_to('results_reset')
        st.rerun()


# --- 「タスク入力」画面 ---
elif st.session_state.page == 'task_input':
    st.title("📥 タスク入力")
    
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun() 
    
    with st.form(key='task_form'):
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
        st.dataframe(df1, use_container_width=True)
        st.info(f"現在、{len(df1)}件のタスクが登録されています。")
    else:
        st.warning("まだ登録されたタスクはありません")

# --- 「引き継ぎ希望申請」画面 ---
elif st.session_state.page == 'application':
    st.title("🙋 引き継ぎ希望申請")
    
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()

    # 登録タスクの表示
    if os.path.isfile("tasks.csv"):
        df = pd.read_csv("tasks.csv")
        
        st.subheader("📋 対象タスク情報")
        st.write("**タスク名:** " + str(df.loc[0, "タスク名"])) 
        st.write("**タスクの詳細:** " + str(df.loc[0, "タスクの詳細"]))
        st.write("**タスクを行う時期・日時:** " + str(df.loc[0, "タスクを行う時期・日時"]))
        st.write("**引き継ぎ担当者:** " + str(df.loc[0, "引き継ぎ担当者"]))
        
        st.divider()

        with st.form(key='evaluate_form'):
            st.subheader("📊 評価入力")
            
            # スライダーで10段階評価する
            contentValue = st.slider(
                'タスクの内容に関する評価', 0, 10, key='content'
            )
            personValue = st.slider(
                '引継ぎ相手に関する評価', 0, 10, key='person'
            )
            scheduleValue = st.slider(
                'スケジュールに関する評価', 0, 10, key='schedule'
            )

            # 提出ボタン
            submitted = st.form_submit_button("提出")

            # 保存処理
            if submitted:
                if contentValue * personValue * scheduleValue != 0:
                    # csvにデータを書き込み
                    DATA_FILE2 = "tasks2.csv"

                    # 評価データ
                    if os.path.isfile("tasks2.csv"):
                        personIndex = len(pd.read_csv("tasks2.csv")) + 1
                    else:
                        personIndex = 1
                    
                    data2 = pd.DataFrame(
                        [["匿名" + str(personIndex), df.loc[0, "タスク名"], contentValue, personValue, scheduleValue]], 
                        columns=["人名", "タスク名", "タスクの内容に関する10段階評価", "引き継ぎ相手に関する10段階評価", "スケジュールに関する評価"]
                    )  
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
    

                    if not os.path.isfile(DATA_FILE2):
                        data2.to_csv(DATA_FILE2, index=False, encoding='utf-8-sig')
                    else:
                        data2.to_csv(DATA_FILE2, mode='a', header=False, index=False, encoding='utf-8-sig')
                
                    # 成功表示
                    st.success("評価が完了しました。")
                    st.balloons()
                    
                    # ホームに戻る
                    navigate_to('main')
                    st.rerun()
                    
                # 評価していない項目があれば警告
                else:
                    st.error("全評価を1~10段階で行ってください。")
    else:
        st.warning("まだ登録されたタスクがありません。先にタスクを登録してください。")

# --- 「最適な引き継ぎ先の確認・情報リセット」画面 ---
elif st.session_state.page == 'results_reset':
    st.title("🧹 最適な引き継ぎ先の確認・情報リセット")

    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()

    if os.path.isfile("tasks.csv") and os.path.isfile("tasks2.csv"):
        df1 = pd.read_csv("tasks.csv")
        df2 = pd.read_csv("tasks2.csv")

        st.subheader("📊 最適な引き継ぎ先一覧")

        best_pairing, total_score = solve_matching(df2, df1)
        if best_pairing:
            st.success(f"全体の合計スコアが最大（{round(total_score, 2)}点）になる組み合わせを算出しました！")
            result_df = pd.DataFrame(best_pairing)
            st.table(result_df)
        
        else:
            st.warning("条件を満たす組み合わせが見つかりませんでした。評価を緩めるか、回答を増やしてください。")

    else:
        st.error("データが見つかりません。tasks.csv と tasks2.csv の両方が必要です。")
    
    st.divider()
    
    if st.button("🗑️ データのリセット", type="secondary"):
        if os.path.exists("tasks.csv"): 
            os.remove("tasks.csv")
        if os.path.exists("tasks2.csv"): 
            os.remove("tasks2.csv")
        st.warning("全てのデータを削除しました。")
        st.rerun()
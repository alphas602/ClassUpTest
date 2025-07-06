import streamlit as st
import random
from utils.csv_handler import load_csv_data, load_all_csv_files
import MissedUtil as MU
import os

def to_html_with_br(text):
    return text.replace("\n", "<br>")

def main():
    st.set_page_config(layout="wide")  # 画面いっぱい
    #st.title("daigas classup (Streamlit版)")

    # --- セッションで状態管理
    if "app_state" not in st.session_state:
        st.session_state.app_state = "setup"  # "setup" or "quiz"
    if "data" not in st.session_state:
        st.session_state.data = []
    if "mode" not in st.session_state:
        st.session_state.mode = None
    if "selected_files" not in st.session_state:
        st.session_state.selected_files = []
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    # --- セットアップ画面
    if st.session_state.app_state == "setup":
        folder_path = os.path.join(os.path.dirname(__file__), "mondai")
        file_pathes, datanames = load_all_csv_files(folder_path)
        st.markdown("#### 使用するファイルを選択してください")

        checkbox_keys = [f"file_{fname}" for fname in datanames]

        # 初回のみ全選択
        if all(k not in st.session_state for k in checkbox_keys):
            for k in checkbox_keys:
                st.session_state[k] = True

        # 全選択・全解除ボタン
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("すべて選択"):
                for k in checkbox_keys:
                    st.session_state[k] = True
                st.rerun()
        with col_b:
            if st.button("すべて解除"):
                for k in checkbox_keys:
                    st.session_state[k] = False
                st.rerun()

        # 各ファイルごとにチェックボックス（key管理のみ、value不要）
        for fname, k in zip(datanames, checkbox_keys):
            st.checkbox(fname, key=k)
        # 選択されたファイル名リストをkeyから再構築
        st.session_state.selected_files = [fname for fname, k in zip(datanames, checkbox_keys) if st.session_state.get(k, False)]
        selected_files = st.session_state.selected_files

        # ラジオボタンもkeyで管理
        if "mode_radio" not in st.session_state:
            st.session_state.mode_radio = "順番に出題"
        mode = st.radio("出題モードを選択してください", ("順番に出題", "ランダムに出題", "missed_question.csvから出題"), key="mode_radio")

        if st.button("データを読み込んで開始"):
            valid_file_names = selected_files
            data = []
            missed_path = os.path.join(os.path.dirname(__file__), "mondai", "missed_question", "missed_question.csv")
            if mode == "missed_question.csvから出題":
                if os.path.isfile(missed_path):
                    data = load_csv_data(missed_path)
                else:
                    st.warning("missed_question.csvが見つかりません。")
            else:
                for file_path, file_name in zip(file_pathes, datanames):
                    if file_name in valid_file_names:
                        data.extend(load_csv_data(file_path))
                if mode == "ランダムに出題":
                    random.shuffle(data)

            if data:
                st.session_state.data = data
                st.session_state.mode = mode
                st.session_state.selected_files = selected_files
                st.session_state.current_question_index = 0
                st.session_state.app_state = "quiz"
                st.rerun()
            else:
                st.warning("出題できる問題がありません。")
        st.stop()  # ここでUIを止める

    # --- 問題出題画面
    data = st.session_state.data
    qidx = st.session_state.current_question_index

    # 画面いっぱい中央に
    st.markdown("""
    <style>
    /* ページ全体を上寄せにする */
    body, .main, .block-container {
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        min-height: 100vh;
    }

    /* markdownテキストのサイズを小さく */
    .stMarkdown, .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
        font-size: 0.95em !important;
    }

    /* 問題・答えの枠 */
    .big-question {
        font-size: 1em;
        margin: 1em 0;
        border: 2px solid #888;
        border-radius: 8px;
        padding: 12px;
        background: #f9f9f9;
        box-shadow: 2px 2px 6px #eee;
        color: #111;
    }
    .big-answer {
        font-size: 0.92em;
        margin: 1em 0;
        border: 1.5px solid #aaa;
        border-radius: 6px;
        padding: 10px;
        background: #fcfcfc;
        color: #111;
    }
    </style>
    """, unsafe_allow_html=True)


    st.markdown(
        f'<div style="font-size:0.9em; color:#fff; margin-bottom:0.5em;">ファイル名: {data[qidx]["FileName"]}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="big-question">{to_html_with_br(data[qidx]["Question"])}</div>',
        unsafe_allow_html=True
    )

    # 答え表示状態をセッションで管理
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    # 問題が切り替わったら答え非表示にリセット
    if "last_qidx" not in st.session_state or st.session_state.last_qidx != qidx:
        st.session_state.show_answer = False
        st.session_state.last_qidx = qidx

    if st.session_state.show_answer:
        st.markdown(
            f'<div class="big-answer" style="color:#111;">{to_html_with_br(data[qidx]["Answer"])}</div>',
            unsafe_allow_html=True
        )
        next_label = "次へ"
    else:
        st.markdown(
            f'<div class="big-answer" style="color:#fff;">{to_html_with_br(data[qidx]["Answer"])}</div>',
            unsafe_allow_html=True
        )
        next_label = "答えを見る"

    # ナビゲーション
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(next_label):
            if not st.session_state.show_answer:
                st.session_state.show_answer = True
            else:
                if qidx < len(data) - 1:
                    st.session_state.current_question_index += 1
                    st.session_state.show_answer = False
            st.rerun()
    with col2:
        if st.button("前へ") and qidx > 0:
            st.session_state.current_question_index -= 1
            st.session_state.show_answer = False
            st.rerun()
    with col3:
        missed_path = os.path.join(os.path.dirname(__file__), "mondai", "missed_question", "missed_question.csv")
        if st.session_state.mode == "missed_question.csvから出題":
            if st.button("問題を間違いリストから削除"):
                MU.delete_missed_data(qidx, data, qidx, missed_path)
                st.success("問題をmissed_question.csvから削除しました。")
                # 削除後のリストを再読み込み
                if os.path.isfile(missed_path):
                    st.session_state.data = load_csv_data(missed_path)
                    if len(st.session_state.data) == 0:
                        st.session_state.app_state = "setup"
                        st.rerun()
                    elif st.session_state.current_question_index >= len(st.session_state.data):
                        st.session_state.current_question_index = max(0, len(st.session_state.data) - 1)
                    st.session_state.show_answer = False
                    st.rerun()
                else:
                    st.session_state.app_state = "setup"
                    st.rerun()
        else:
            if st.button("問題を記憶（missed_question.csvへ）"):
                MU.remember_question(qidx, data, qidx, [], missed_path)
                st.success("問題をmissed_question.csvに記憶しました。")

    # リセット（最初からやり直し）
    if st.button("最初からやり直す"):
        st.session_state.app_state = "setup"
        st.rerun()

if __name__ == "__main__":
    main()

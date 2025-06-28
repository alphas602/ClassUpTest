import random  # ランダム操作のためにインポート
import tkinter as tk
from utils.csv_handler import load_csv_data, load_all_csv_files
from tkinter import ttk
import os  # ファイルパス操作のためにインポート
import csv  # CSVファイルの読み書きのためにインポート

class CsvUiTool:
    def __init__(self, master, folder_path=None):
        if folder_path is None:
            # app.pyから見て../mondai を指す相対パス
            folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mondai")
        self.master = master
        self.master.title("daigas classup")
        self.count = 0
        self.endcount = 0 # 問題終了数を設定するカウント
        self.folder_path = folder_path
        self.missed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mondai", "missed_question", "missed_question.csv")
        self.ValidFileNames = []  # 有効なファイル名を格納するリスト
        self.remember_data = []  # 記憶した問題と回答を格納するリスト

        self.file_pathes,self.datanames = load_all_csv_files(self.folder_path)

        self.open_settings_menu()

    def open_settings_menu(self):
        """設定メニューをmaster上に開き、ファイル名を複数選択できるようにする"""
        # 既存ウィジェットを一旦全て削除
        for widget in self.master.winfo_children():
            widget.destroy()

        # ラベル
        label = tk.Label(self.master, text="使用するファイルを選択してください（複数選択可）")
        label.pack(pady=10)

        # Listbox（複数選択可）
        self.file_listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE, width=40, height=15)
        for name in self.datanames:
            self.file_listbox.insert(tk.END, name)
        self.file_listbox.pack(pady=10)

        # Select ALL/NONEボタン用フレーム
        select_frame = tk.Frame(self.master)
        select_frame.pack(pady=5)

        # Select ALLボタン
        select_all_btn = tk.Button(select_frame, text="Select ALL", command=self.select_all_files)
        select_all_btn.pack(side="left", padx=5)

        # Select NONEボタン
        select_none_btn = tk.Button(select_frame, text="Select NONE", command=self.select_none_files)
        select_none_btn.pack(side="left", padx=5)

        # OKボタン
        ok_button = tk.Button(self.master, text="OK", command=self.confirm_file_selection)
        ok_button.pack(pady=10)

    def select_all_files(self):
        """リストボックスの全項目を選択（NONE以外）"""
        self.file_listbox.select_set(0, tk.END)

    def select_none_files(self):
        """リストボックスの全選択を解除"""
        self.file_listbox.selection_clear(0, tk.END)
    
    def confirm_file_selection(self):
        """選択されたファイル名をValidFileNamesリストに追加し、設定画面を消して初期画面を表示"""
        selected_indices = self.file_listbox.curselection()
        self.ValidFileNames = [self.datanames[i] for i in selected_indices]

        # 設定画面のウィジェットを削除
        for widget in self.master.winfo_children():
            widget.destroy()

        # 初期画面を表示
        self.initialmode()
        self.init_buttons()

        # Enterキーで回答を表示するように設定
        self.master.bind("<Return>", self.refresh_display)

        # "[" キーで今出題中の問題を記憶するように設定
        self.master.bind("<KeyPress-[>", self.remember_question)

        # "d" キーで現在の問題をmissed_question.csvから削除するように設定
        self.master.bind("<KeyPress-d>", self.delete_missed_data)


    def initialmode(self):
        self.mode = tk.StringVar(value="normal")
        self.mode_label = tk.Label(self.master, text="出題モードを選択して下さい:")
        self.mode_label.pack()

        # 横並び用のフレームを作成
        mode_frame = tk.Frame(self.master)
        mode_frame.pack(pady=10)

        self.normal_mode_button = tk.Radiobutton(
            mode_frame, text="順番に出題", variable=self.mode, value="normal", command=self.set_mode
        )
        self.normal_mode_button.pack(side="left", padx=10)

        self.random_mode_button = tk.Radiobutton(
            mode_frame, text="ランダムに出題", variable=self.mode, value="random", command=self.set_mode
        )
        self.random_mode_button.pack(side="left", padx=10)

        self.miss_mode_button = tk.Radiobutton(
            mode_frame, text="missed_question.csvから出題", variable=self.mode, value="missed", command=self.set_mode
        )
        self.miss_mode_button.pack(side="left", padx=10)

    def init_buttons(self):
        # ボタンを横並びにするフレームを作成
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5)

        # 開始ボタン
        self.start_button = tk.Button(button_frame, text="開始", command=self.start_quiz)
        self.start_button.pack(side="left", padx=10)

        # ファイル名選択ボタン
        self.file_select_button = tk.Button(button_frame, text="ファイル選択", command=self.open_settings_menu)
        self.file_select_button.pack(side="left", padx=10)

        # タイトル
        self.Title = tk.Label(self.master, text="Questions from CSV:")
        self.Title.pack()
        self.Title.config(
            font=("Arial", 32, "bold"),
            fg="blue",
            bg="lightgray",
            padx=20,
            pady=20,
            borderwidth=2,
            relief="groove",
            anchor="center",
            width=40,
            height=1,
            cursor="hand2",
            highlightthickness=2,
            highlightbackground="black",
            highlightcolor="red",
            underline=True
        )
        
        # 問題用のスクロール可能なテキストエリア
        self.question_text = tk.Text(
            self.master,
            wrap="word",
            font=("Arial", 20),
            fg="black",
            bg="white",
            padx=10,
            pady=10,
            borderwidth=1,
            relief="solid",
            width=100,
            height=12,
            cursor="arrow",
            highlightthickness=1,
            highlightbackground="gray",
            highlightcolor="blue",
        )
        self.question_text.pack()
        self.question_scroll = ttk.Scrollbar(self.master, command=self.question_text.yview)
        self.question_scroll.pack(side="right", fill="y")
        self.question_text["yscrollcommand"] = self.question_scroll.set

        # 回答用のスクロール可能なテキストエリア
        self.answer_text = tk.Text(
            self.master,
            wrap="word",
            height=10,
            width=80,
            font=("Arial", 20),
            fg="black",
            bg="white",
            padx=10, 
            pady=10,
            borderwidth=1, 
            relief="solid",
        )
        self.answer_text.pack()
        self.answer_scroll = ttk.Scrollbar(self.master, command=self.answer_text.yview)
        self.answer_scroll.pack(side="right", fill="y")
        self.answer_text["yscrollcommand"] = self.answer_scroll.set

    def set_mode(self):
        """モードを設定する（ラジオボタンの選択時に呼び出される）"""
        print(f"選択されたモード: {self.mode.get()}")  # デバッグ用

    def set_data(self):
        self.data = []
        if self.mode.get() == "missed":
            # missed_question.csvからデータを読み込む
            if os.path.isfile(self.missed_path):
                self.data = load_csv_data(self.missed_path)
            else:
                print("missed_question.csvが見つかりません。")
        else:
            # self.ValidFileNames に該当するファイルだけデータを追加
            for file_path, file_name in zip(self.file_pathes, self.datanames):
                if file_name in self.ValidFileNames:
                    self.data.extend(load_csv_data(file_path))  # 各ファイルのデータを self.data に追加

            # ランダムモードの場合、データをシャッフル
            if self.mode.get() == "random":
                random.shuffle(self.data)

    def start_quiz(self):
        """クイズを開始する"""
        # データをロード
        self.set_data()
        # 最初の質問を表示
        self.current_question_index = 0
        self.endcount = 0
        self.set_question()

    def set_Title(self):
        """タイトルを設定する"""
        if self.data:
            # 最初のファイル名をタイトルに設定
            self.Title.config(text=self.data[self.current_question_index]['FileName'])
        else:
            self.Title.config(text="No questions available.")

    def set_question(self):
        if self.current_question_index < len(self.data):
            # 一時的に編集可能にする
            self.question_text.config(state="normal")
            self.question_text.delete("1.0", tk.END)  # テキストエリアをクリア
            self.question_text.insert(tk.END, self.data[self.current_question_index]['Question'])
            self.set_Title()  # タイトルを更新
            # 再び編集不可にする
            self.question_text.config(state="disabled")

            # 回答エリアをクリア
            self.answer_text.config(state="normal")
            self.answer_text.delete("1.0", tk.END)
            self.answer_text.config(state="disabled")
        else:
            self.question_text.config(state="normal")
            self.question_text.delete("1.0", tk.END)
            self.question_text.insert(tk.END, "No more questions.")
            self.question_text.config(state="disabled")

            self.answer_text.config(state="normal")
            self.answer_text.delete("1.0", tk.END)
            self.answer_text.config(state="disabled")

    def set_answer(self):
        if self.current_question_index < len(self.data):
            answer = self.data[self.current_question_index]['Answer']
            # 一時的に編集可能にする
            self.answer_text.config(state="normal")
            self.answer_text.delete("1.0", tk.END)  # テキストエリアをクリア
            self.answer_text.insert(tk.END, answer)
            # 再び編集不可にする
            self.answer_text.config(state="disabled")
            self.current_question_index += 1
        else:
            self.answer_text.config(state="normal")
            self.answer_text.delete("1.0", tk.END)
            self.answer_text.insert(tk.END, "No more answers.")
            self.answer_text.config(state="disabled")

    def refresh_display(self, event=None):
        """Enterキーが押されたときに呼び出されるメソッド"""
        self.count += 1
        if self.count % 2 == 0:
            self.set_question()
            self.endcount += 1
        else:
            self.set_answer()

    def remember_question(self, event=None):
        """現在の問題を記憶し、missed_question.csvに都度出力する"""
        if self.current_question_index < len(self.data) and self.MissedDataIsRedundant(self.data[self.endcount])==False:
            question = self.data[self.endcount]['Question']
            answer = self.data[self.endcount]['Answer']
            file_name = self.data[self.endcount]['FileName']
            self.remember_data.append({'問題': question, '解答': answer, 'ファイル名': file_name})
            print(f"問題: {question}, 解答: {answer}, ファイル名: {file_name}")

            # 保存先パスを指定
            file_exists = os.path.isfile(self.missed_path)
            with open(self.missed_path, mode="a", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["問題", "解答", "ファイル名"])
                if not file_exists:
                    writer.writeheader()
                writer.writerow({'問題': question, '解答': answer, 'ファイル名': file_name})
        else:
            print("現在の問題がないか、問題が重複しています")

    def delete_missed_data(self, event=None):
        """現在表示されている問題をmissed_question.csvから削除する"""
        if self.current_question_index < len(self.data):
            question = self.data[self.endcount]['Question']
            answer = self.data[self.endcount]['Answer']
            file_name = self.data[self.endcount]['FileName']
            if self.MissedDataIsRedundant(self.data[self.endcount]):
                # missed_question.csvから削除する
                if os.path.isfile(self.missed_path):
                    with open(self.missed_path, mode="r", encoding="utf-8", newline="") as f:
                        reader = csv.DictReader(f)
                        rows = [row for row in reader if not (row["問題"] == question and row["解答"] == answer and row["ファイル名"] == file_name)]
                    # 一時ファイルに書き込む
                    with open(self.missed_path, mode="w", encoding="utf-8", newline="") as f:
                        writer = csv.DictWriter(f, fieldnames=["問題", "解答", "ファイル名"])
                        writer.writeheader()
                        writer.writerows(rows)
            else:
                print("現在の問題はmissed_question.csvに存在しません。削除できません。")


    def MissedDataIsRedundant(self, data):
        """
        missed_question.csvに記載されている問題をチェックし、
        「問題」「解答」「ファイル名」がすべて一致する行がある場合はTrueを返す
        """
        if os.path.isfile(self.missed_path):
            with open(self.missed_path, encoding="utf-8", newline="") as f:
                import csv
                reader = csv.DictReader(f)
                for row in reader:
                    if (
                        row["問題"] == data["Question"]
                        and row["解答"] == data["Answer"]
                        and row["ファイル名"] == data["FileName"]
                    ):
                        return True
        return False
import random  # ランダム操作のためにインポート
import tkinter as tk
from utils.csv_handler import load_csv_data, load_all_csv_files
from tkinter import ttk

class CsvUiTool:
    def __init__(self, master, folder_path="C:\\Users\\yoshi\\temp\\csv-ui-tool\\mondai"):
        self.master = master
        master.title("daigas classup")
        self.count = 0
        self.folder_path = folder_path

        self.label = tk.Label(master, text="Questions from CSV:")
        self.label.pack()
        self.label.config(
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

        self.question_text = tk.Text(master, wrap="word", height=10, width=80)
        self.question_text.config(
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

        self.question_scroll = ttk.Scrollbar(master, command=self.question_text.yview)
        self.question_scroll.pack(side="right", fill="y")
        self.question_text["yscrollcommand"] = self.question_scroll.set

        # 回答用のスクロール可能なテキストエリア
        self.answer_text = tk.Text(master, wrap="word", height=10, width=80)
        self.answer_text.config(
            font=("Arial", 20),
            fg="black",
            bg="white",
            padx=10, 
            pady=10,
            borderwidth=1, 
            relief="solid",
        )
        self.answer_text.pack()

        self.answer_scroll = ttk.Scrollbar(master, command=self.answer_text.yview)
        self.answer_scroll.pack(side="right", fill="y")
        self.answer_text["yscrollcommand"] = self.answer_scroll.set


        # Enterキーで回答を表示するように設定
        master.bind("<Return>", self.refresh_display)
        
        self.datas=load_all_csv_files(self.folder_path)
        self.data = []
        for file_path in self.datas:
            self.data.extend(load_csv_data(file_path))  # 各ファイルのデータを self.data に追加
        
        
        self.shuffle_data()
        self.current_question_index = 0
        self.set_question()

    def set_question(self):
        if self.current_question_index < len(self.data) and self.count%2 == 0:
            # 一時的に編集可能にする
            self.question_text.config(state="normal")
            self.question_text.delete("1.0", tk.END)  # テキストエリアをクリア
            self.question_text.insert(tk.END, self.data[self.current_question_index]['Question'])
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
        if self.current_question_index < len(self.data) and self.count % 2 == 1:
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
        else:
            self.set_answer()

    def shuffle_data(self):
        """self.data の行をランダムに入れ替える"""
        random.shuffle(self.data)
        self.current_question_index = 0  # インデックスをリセット
        self.set_question()  # 最初の問題を表示
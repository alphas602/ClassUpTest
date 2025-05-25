import random  # ランダム操作のためにインポート
import tkinter as tk
from utils.csv_handler import load_csv_data, load_all_csv_files


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

        self.question_var = tk.StringVar()
        self.question_label = tk.Label(master, textvariable=self.question_var, wraplength=1300)
        self.question_label.pack()
        self.question_label.config(
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
            justify="left"
        )

        self.answer_var = tk.StringVar()
        self.answer_label = tk.Label(self.master, textvariable=self.answer_var, wraplength=800)
        self.answer_label.pack()
        self.answer_label.config(
            font=("Arial", 20),
            fg="black",
            bg="white",
            padx=10, 
            pady=10,
            borderwidth=1, 
            relief="solid"
        )

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
            self.question_var.set(self.data[self.current_question_index]['Question'])
            self.answer_var.set("")  # 回答ラベルをクリア
        else:
            self.question_var.set("No more questions.")
            self.answer_var.set("")

    def set_answer(self):
        if self.current_question_index < len(self.data) and self.count%2 == 1:
            answer = self.data[self.current_question_index]['Answer']
            self.answer_var.set(answer)
            self.current_question_index += 1
        else:
            self.answer_var.set("No more answers.")

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
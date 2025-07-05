import os
import csv

def remember_question(current_question_index, data, endcount, remember_data, missed_path, event=None):
    """現在の問題を記憶し、missed_question.csvに都度出力する"""
    if current_question_index < len(data) and MissedDataIsRedundant(missed_path,data[endcount])==False:
        question = data[endcount]['Question']
        answer = data[endcount]['Answer']
        file_name = data[endcount]['FileName']
        remember_data.append({'問題': question, '解答': answer, 'ファイル名': file_name})
        print(f"問題: {question}, 解答: {answer}, ファイル名: {file_name}")

        # 保存先パスを指定
        file_exists = os.path.isfile(missed_path)
        with open(missed_path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["問題", "解答", "ファイル名"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({'問題': question, '解答': answer, 'ファイル名': file_name})
    else:
        print("現在の問題がないか、問題が重複しています")

def delete_missed_data(current_question_index, data, endcount, missed_path, event=None):
    """現在表示されている問題をmissed_question.csvから削除する"""
    if current_question_index < len(data):
        question = data[endcount]['Question']
        answer = data[endcount]['Answer']
        file_name = data[endcount]['FileName']
        if MissedDataIsRedundant(missed_path,data[endcount]):
            # missed_question.csvから削除する
            if os.path.isfile(missed_path):
                with open(missed_path, mode="r", encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    rows = [row for row in reader if not (row["問題"] == question and row["解答"] == answer and row["ファイル名"] == file_name)]
                # 一時ファイルに書き込む
                with open(missed_path, mode="w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=["問題", "解答", "ファイル名"])
                    writer.writeheader()
                    writer.writerows(rows)
        else:
            print("現在の問題はmissed_question.csvに存在しません。削除できません。")


def MissedDataIsRedundant(missed_path, data):
    """
    missed_question.csvに記載されている問題をチェックし、
    「問題」「解答」「ファイル名」がすべて一致する行がある場合はTrueを返す
    """
    if os.path.isfile(missed_path):
        with open(missed_path, encoding="utf-8", newline="") as f:
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
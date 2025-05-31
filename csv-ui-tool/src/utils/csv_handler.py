import pandas as pd
import chardet
import os

def load_csv_data(file_path):
    try:
        # ファイルのエンコーディングを検出
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']

        # 検出したエンコーディングでCSVを読み込む
        df = pd.read_csv(file_path, encoding=encoding, header=0)  # ヘッダーを読み込む

        # 「問題」と「解答」の列を特定
        question_col = None
        answer_col = None
        for col_index, col_name in enumerate(df.columns):
            if "問題" in str(col_name):
                question_col = col_index
            if "解答" in str(col_name):
                answer_col = col_index

        # 必要な列が見つからない場合のエラーハンドリング
        if question_col is None or answer_col is None:
            raise ValueError("CSV ファイルに「問題」または「解答」の列が見つかりません。")

        #　「問題」もしくは「解答」の列が空でない行のみを抽出
        df = df.dropna(subset=[df.columns[question_col], df.columns[answer_col]])

        # ファイル名（拡張子なし）を取得
        base_filename = os.path.splitext(os.path.basename(file_path))[0]

        # データをリスト形式で返す
        data = []
        for _, row in df.iterrows():
            data.append({
                'Question': row[question_col],
                'Answer': row[answer_col],
                'FileName': base_filename
            })
        return data

    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []
    
def load_all_csv_files(folder_path):
    """指定フォルダ内のすべてのCSVファイルのパスをリストとして返す"""
    csv_files = []
    csv_file_names = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):  # .csv ファイルのみ対象
            file_path = os.path.join(folder_path, file_name)
            csv_files.append(file_path)  # ファイルパスをリストに追加
            base_name = os.path.splitext(file_name)[0]  # 拡張子なしファイル名
            csv_file_names.append(base_name)
    
    return csv_files,csv_file_names

def extract_questions(data):
    if data is not None:
        # Assuming the first column contains the questions
        return data.iloc[:, 1].tolist()  # Adjust the index based on the actual structure
    return []

def extract_answers(data):
    if data is not None:
        # Assuming the second column contains the answers
        return data.iloc[:, 2].tolist()  # Adjust the index based on the actual structure
    return []

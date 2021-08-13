#　課題１
# １．入力したキーワードで、キャラクターリスト(source)を検索して、存在すれば存在する旨を、存在しなければ存在しない旨をPrint文で表示してみましょう
# ２．１に追加して結果が存在しなかった場合に、キャラクターリスト(source)に追加できるようにしてみましょう
# ３．２に追加してキャラクターリスト(source)をCSVから読み込んで登録できるようにしてみましょう
# ４．３に追加してキャラクターリスト(source)をCSVに書き込めるようにしてみましょう
import os
SOURCE_CSV_PATH = "source.csv"
DEFAULT_CARACTORS = ['ぜんいつ','たんじろう','ねずこ','いのすけ']

def read_source(csv_path : str):
    if not os.path.exists(csv_path):
        print(f"csv_path:(csv_path)が存在しません、新規作成します。")
        write_source(csv_path, DEFAULT_CARACTORS)
    with open(csv_path,'r',encoding="utf-8_sig") as f:
        return f.read().splitlines()

def write_source(csv_path:str,source:list):
    with open(csv_path,"w",encoding="utf-8_sig") as f:
        f.write("\n".join(source))

def search():
    source = read_source(SOURCE_CSV_PATH)
    while True:
        word = input('鬼滅の刃の登場人物を入力>> ')
        if word in source:
            print(f"『{word}』は登録されています")
        else:
            print(f"『{word}』は未登録です")
            is_add=input("追加しますか？(n:しない y:する)>> ")
            if is_add == "y":
                source.append(word)
        write_source(SOURCE_CSV_PATH, [word])

if __name__ == "__main__":
    search()

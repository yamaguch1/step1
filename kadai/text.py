# 課題０
# 変数を使って、「ねずこ」と「ぜんいつ」 は仲間ですとprint文を使って表示させてみよう
# なお、ねずこをname1、ぜんいつをname2として定義してください。
name1 = 'ねずこ'
name2 = 'ぜんいつ'
print(name1 + 'と' + name2 + 'は仲間です')
# １のソースを改造して、name2が敵キャラの「むざん」だった場合に
# 仲間ではありませんと表示させてみよう。
name2 = 'むざん'
if name2 =='むざん':
    print('仲間ではありません')
# 以下の配列に対して、キャラクター「ぜんいつ」を追加してみよう。 appendを使うことで追加できます。 name=["たんじろう","ぎゆう","ねずこ","むざん"]
names = ['たんじろう','ぎゆう','ねずこ','むざん']
names.append('ぜんいつ')
# ３のソースコードで使用したnameのキャラクターをfor文を使って
# １行に１キャラクター表示してみよう
for name in names:
    print(name)
# 以下のようにhikisuuの部分が引数です。引数は関数の外から変数を関数内に渡すことができます。
def test(hiki):
    result = hiki in names
    if result == True:
        print(f"{hiki} は含まれます")
test('ぎゆう')

def test2(hiki):
    if hiki in names:
        print("OK")
    else:
        print(hiki + "" "No")

test2("ぎゆう")
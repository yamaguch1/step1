#位置引数の辞書化
def say_something(word,*args):
    print(word)
    for arg in args:
        print(arg)
say_something('hi!','Mike','Nancy')

#キーワード引数の辞書化
def menu1(**kwargs):
    print(kwargs)
menu1(entree='beef',drink='coffee')

#print(kwargs)をforにする
def menu2(**kwargs):
    for k,v in kwargs.items():
        print(k,v)
menu1(entree='beef',drink='coffee')

#辞書を入れるのと同じ
def menu3(**kwargs):
    print(kwargs)
d={'entree':'beef',
'drink':'coffee'
}
menu3(**d)

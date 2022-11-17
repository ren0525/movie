# -*- coding: utf-8 -*-

from gensim.summarization.bm25 import BM25
from janome.tokenizer import Tokenizer
import demoji
import MeCab
wakati_list = []

movie_name = ['シンゴジラ', 'シンウルトラマン', 'トップガン', 'パラサイト']
filenames = ['text/review_in_godzilla.txt','text/review_in_ultraman.txt', 'text/review_in_topgun.txt', 'text/review_in_parasite.txt']
class best_match:
    def __init__(self):
        self.t = MeCab.Tagger()

    #前処理
    def pre_process(self, docs):
        self.docs = docs
        corpus = [self.wakachi(doc) for doc in self.docs]
        self.bm25_ = BM25(corpus)
    
    #クエリとの順位付け
    def ranking(self, query):
        wakachi_query = self.wakachi(query)
        self.scores = self.bm25_.get_scores(wakachi_query)

    #分かち書き
    def wakachi(self, doc):
        word_list = []
        for row in self.t.parse(doc).split("\n"):
            word =row.split("\t")[0]#タブ区切りになっている１つ目を取り出す。ここには形態素が格納されている
            if word == "EOS":
                break
            else:
                pos = row.split("\t")[1].split(',')#タブ区切りになっている2つ目を取り出す。ここには品詞が格納されている
                if ("名詞" in pos and '一般' in pos and '非自立' not in pos) or ("名詞" in pos and '固有名詞' in pos and '非自立' not in pos) or '形容詞' in pos:
                    word_list.append(word) 
        return word_list

    #上位n件を抽出
    def select_docs(self, num):
        docs_dict = dict(zip(self.scores, movie_name))
        docs_dict = dict(sorted(docs_dict.items(), reverse = True))
        print("\n・検索結果")
        print(docs_dict.keys())
        i = 0
        for key, value in docs_dict.items():
            print(round(key, 3), value[:100])
            i += 1
            if i == num: 
                break

if __name__ == "__main__":
    query = 'ゴジラ、怖い、わくわくする'
    docs = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as f:
            text = demoji.replace(f.read(), repl='')
            docs.append(text)
    while True:
        try:
            num = int(input("検索数を自然数で入力してください:"))
            if num <= 0:
                print("0より大きな数字を入力してください。")
            elif num <= len(docs):
                break
            else:
                print("文書数より多い数字が入力されています。")
        except Exception:
            print("数字以外のテキストが入力されています。")

    print("クエリ:", query)
    inst_BM = best_match()
    inst_BM.pre_process(docs)
    inst_BM.ranking(query)
    inst_BM.select_docs(num)

# -*- coding: utf-8 -*-
from gensim.summarization.bm25 import BM25
from janome.tokenizer import Tokenizer
import demoji
import MeCab
import openpyxl

wakati_list = []
movie_name = ['シンゴジラ', 'フォレストガンプ', 'トップガン', 'パラサイト', 'タイタニック',
              'シンウルトラマン', 'ゴッドファーザー', 'ロッキー', 'マイフェアレディ', 'ウエストサイドストーリー',
              'テリファー', 'レプリカズ', 'デイシフト', 'バーフバリ', 'スケートキッチン']
file_name = ['text/popular/review_in_godzilla.txt','text/popular/review_in_forrestgump.txt','text/popular/review_in_topgun.txt', 'text/popular/review_in_parasite.txt', 'text/popular/review_in_titanic.txt', 'text/review.txt',
            'text/standard/review_in_ultraman.txt', 'text/standard/review_in_godfather.txt', 'text/standard/review_in_rocky.txt', 'text/standard/review_in_myfairlady.txt', 'text/standard/review_in_westsidestory.txt',
            'text/unpopular/review_in_terrifier.txt', 'text/unpopular/review_in_replicas.txt', 'text/unpopular/review_in_baahubali.txt', 'text/unpopular/review_in_dayshift.txt', 'text/unpopular/review_in_skatekitchen.txt']

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
        print(wakachi_query)
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
    def select_docs(self):
        docs_dict = dict(zip(self.scores, movie_name))
        docs_dict = dict(sorted(docs_dict.items(), reverse = True))
        print("\n・検索結果")
        i = 0
        for key, value in docs_dict.items():
            print(round(key, 3), value)
            i += 1
            if i == len(movie_name):
                break
        # book = openpyxl.load_workbook('dataframe/movie_recommend_data_xlsx')
        # sheet = book['Sheet1']
        # sheet['C1'] = 'bm25'
        # i = 2
        # for n in range(len(movie_name)):
        #     sheet[f'C{i}'] = self.scores[n]
        #     i += 1
        #     if i == len(movie_name) + 2:
        #         # book.save('dataframe/movie_recommend_data_xlsx') 
        #         print('OK')
                # break

if __name__ == "__main__":
    query = '寂しい　感動　楽しい　爆発　迫力'
    docs = []
    for filename in file_name:
        with open(filename, 'r', encoding='utf-8') as f:
            text = demoji.replace(f.read(), repl='')
            docs.append(text)

    print("クエリ:", query)
    inst_BM = best_match()
    inst_BM.pre_process(docs)
    inst_BM.ranking(query)
    inst_BM.select_docs()

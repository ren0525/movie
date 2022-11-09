import requests
from bs4 import BeautifulSoup
import sys
import MeCab
from time import sleep
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import movie_info as mi
import re
import demoji

# Step2：それらをMeCabで形態素解析。名詞だけ抽出。
def mplg(review):
    word_list = ""
    review = demoji.replace(string=review, repl="")
    m=MeCab.Tagger()
    m1=m.parse(review)
    print(m1)
    for row in m1.split("\n"):
        word =row.split("\t")[0]#タブ区切りになっている１つ目を取り出す。ここには形態素が格納されている
        if word == "EOS":
            break
        else:
            pos = row.split("\t")[1]#タブ区切りになっている2つ目を取り出す。ここには品詞が格納されている
            slice = pos[:2]
            print(slice)
            if slice == "名詞" and slice != '非自立' and slice != '代名詞' and slice != '接尾' and slice != '数':
                word_list = word_list +" "+ word
    print(word_list)
    return word_list

# Step3：名詞の出現頻度からTF-IDF/COS類似度を算出。テキスト情報のマッチ度を測る
def tfidf(word_list):
    docs = np.array(word_list)#Numpyの配列に変換する
    #単語を配列ベクトル化して、TF-IDFを計算する
    vecs = TfidfVectorizer(
                token_pattern=u'(?u)\\b\\w+\\b'#文字列長が 1 の単語を処理対象に含めることを意味します。
                ).fit_transform(docs)
    vecs = vecs.toarray()
    return vecs


def cossim(v1,v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

##実装
word_list=[]
text=open(f'text/review_in_{mi.movie_name}.txt', 'r', encoding='utf-8').read()
word_list.append(mplg(text))

vecs = tfidf(word_list)
print(tfidf(word_list))
print(cossim(vecs[0][2],vecs[0][0]))
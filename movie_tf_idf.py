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
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfTransformer
from janome.tokenizer import Tokenizer


filenames=['text/review_in_godzila.txt','text/review_in_ultraman.txt','text/review_in_topgun.txt']
wakati_list = []
for filename in filenames: # テキストファイルを読み出しtextに代入 
    with open(filename,mode='r',encoding = 'utf-8-sig') as f:
        text = f.read()    
    wakati = ''
    t = Tokenizer() 
    for token in t.tokenize(text):  # 形態素解析
        hinshi = (token.part_of_speech).split(',')[0]  # 品詞情報
        hinshi_2 = (token.part_of_speech).split(',')[1]
        if hinshi in ['名詞']:  # 品詞が名詞の場合のみ以下実行
            if not hinshi_2 in ['空白','*']:  
            # 品詞情報の2項目目が空白か*の場合は以下実行しない
                word = str(token).split()[0]  # 単語を取得
                if not ',*,' in word:  # 単語に*が含まれない場合は以下実行
                    wakati = wakati + word +' ' 
                    # オブジェクトwakatiに単語とスペースを追加 
    wakati_list.append(wakati) # 分かち書き結果をリストに追加
wakati_list_np = np.array(wakati_list) # リストをndarrayに変換
print(wakati_list_np)

vectorizer = TfidfVectorizer(token_pattern=u'\\b\\w+\\b')
transformer = TfidfTransformer()# transformerの生成。TF-IDFを使用
tf = vectorizer.fit_transform(wakati_list_np) # ベクトル化
tfidf = transformer.fit_transform(tf) # TF-IDF
tfidf_array = tfidf.toarray()
cs = cosine_similarity(tfidf_array,tfidf_array)  # cos類似度計算
print(cs)
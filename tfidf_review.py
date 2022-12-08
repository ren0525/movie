#必要なモジュールをインポート
import pandas as pd
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from numpy import dot 
from numpy.linalg import norm 
from scipy import spatial
import demoji
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import MeCab


#pandasライブラリで読み込み。自動的にカラム名設定。
df = pd.read_excel("dataframe/review_data.xlsx", usecols="B:K").values.tolist()

wakati_list = []
cos_list = []
adjustment_cosine_similarity = []
movie_name = ['シンゴジラ', 'フォレストガンプ', 'トップガン', 'パラサイト', 'タイタニック',
              'シンウルトラマン', 'ゴッドファーザー', 'ロッキー', '2001年宇宙の旅', 'ウエストサイドストーリー',
              'マリグナント', 'イコライザー', 'グレムリン', '孤狼の血', '羊たちの沈黙' ]

            
for review in df:
    word_list = ''
    result = ' '.join(map(str, review))
    text_1 = demoji.replace(string=result, repl="")
    m=MeCab.Tagger()
    m1=m.parse(text_1)
    for row in m1.split("\n"):
        word =row.split("\t")[0]#タブ区切りになっている１つ目を取り出す。ここには形態素が格納されている
        if word == "EOS":
            break
        elif word == 'nan':
            continue
        else:
            pos = row.split("\t")[1].split(',')#タブ区切りになっている2つ目を取り出す。ここには品詞が格納されている
            if ("名詞" in pos and '一般' in pos and '非自立' not in pos) or ("名詞" in pos and '固有名詞' in pos and '非自立' not in pos) in pos:
                word_list = word_list + ' ' + word 
    wakati_list.append(word_list)
wakati_list_np = np.array(wakati_list) # リストをndarrayに変換



# vectorizerの生成。token_pattern=u'\\b\\w+\\b'で1文字の語を含む設定
vectorizer = CountVectorizer(token_pattern=u'\\b\\w+\\b')
# transformerの生成。TF-IDFを使用
transformer = TfidfTransformer()
tf = vectorizer.fit_transform(wakati_list_np) # ベクトル化
tfidf = transformer.fit_transform(tf) # TF-IDF
tfidf_array = tfidf.toarray()
cos = cosine_similarity(tfidf_array,tfidf_array)  # cos類似度計算

# print(review_matrix)
print(np.round(cos, decimals=3))

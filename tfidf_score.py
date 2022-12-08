#必要なモジュールをインポート
import pandas as pd
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from numpy import dot 
from numpy.linalg import norm 
from scipy import spatial


#pandasライブラリで読み込み。自動的にカラム名設定。
df = pd.read_excel("dataframe/score_data.xlsx", usecols="B:P")

rating_matrix_item = np.array(df)

score_list = []
new_rating_list = []
adjustment_cosine_similarity = []
movie_name = ['シンゴジラ', 'フォレストガンプ', 'トップガン', 'パラサイト', 'タイタニック',
              'シンウルトラマン', 'ゴッドファーザー', 'ロッキー', '2001年宇宙の旅', 'ウエストサイドストーリー',
              'マリグナント', 'イコライザー', 'グレムリン', '孤狼の血', '羊たちの沈黙' ]

for i in rating_matrix_item:
    n = sum(1 for x in i if x>0)
    average_score = sum(i) / n
    for j in i:
        if j > 0:
            score_list.append(j - average_score)
        else:
            score_list.append(0.0)
    new_rating_list.append(score_list)
    score_list = []

new = np.array(new_rating_list).T
m = -1
l = 0
while l < 15:
    for i in range(len(movie_name)):
        num = []
        for (k,v) in zip(new[l],new[i]):
            m += 1
            if k == 0:
                continue
            elif k != 0 and m not in num:
                num.append(m)
                if v == 0 and m in num:
                    num.remove(m)
            elif v != 0 and m not in num:
                num.append(m) 

        m = -1
        array1 =[]
        array2 =[]
        for x in num:
            array1.append(np.round(new[l][x], decimals=2))
            array2.append(np.round(new[i][x], decimals=2))
        
        cos_sim = cosine_similarity([array1], [array2])
        score_list.append(cos_sim[0][0]) 
    adjustment_cosine_similarity.append(score_list)
    score_list = [] 
    l += 1

print(rating_matrix_item)
print(np.round(adjustment_cosine_similarity, decimals=3))

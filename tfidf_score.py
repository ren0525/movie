#必要なモジュールをインポート
import pandas as pd
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing

#pandasライブラリで読み込み。自動的にカラム名設定。
df = pd.read_excel("dataframe/score_data.xlsx", usecols="B:P")

rating_matrix_item = np.array(df)

score_list = []
new_rating_list = []
adjustment_cosine_similarity = []
movie_name = ['シンゴジラ', 'フォレストガンプ', 'トップガン', 'パラサイト', 'タイタニック',
              'シンウルトラマン', 'ゴッドファーザー', 'ロッキー', '2001年宇宙の旅', 'ウエストサイドストーリー',
              'テリファー', 'レプリカズ', 'デイシフト', '孤狼の血', '羊たちの沈黙', ]


# for i in rating_matrix_item:
#     n = sum(1 for x in i if x>0)
#     average_score = sum(i) / n
#     for j in i:
#         if j > 0:
#             score_list.append(j - average_score)
#         else:
#             score_list.append(0.0)
#     new_rating_list.append(score_list)
#     score_list = []


# # コサイン
# similarity_matrix = cosine_similarity(np.array(rating_matrix_item).T)
# print(similarity_matrix)

# jaccard
# similarity_matrix = 1 - pairwise_distances(rating_matrix_item, metric='jaccard')

# 対角成分の値はゼロにする
# print(np.fill_diagonal(similarity_matrix, 0))
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


from numpy import dot 
from numpy.linalg import norm 
new = np.array(new_rating_list).T
print(new_rating_list)
print(new)
m = 0
l = 0
yu = []
while l < 15:
    for i in range(len(movie_name)):
        for (k,v) in zip(new[l],new[i]):
            if k == 0 and m not in yu:
                yu.append(m)
            
            if v == 0:
                if m not in yu:
                    yu.append(m) 
                m += 1
            else:
                m += 1
        m = 0
        for x in yu:
            array1 =[]
            array2 =[]
            array1.append(new[l])

        print(array2)
        print(array1)
        cos_sim = cosine_similarity([array1], [array2])
        score_list.append(cos_sim) 
    adjustment_cosine_similarity.append(score_list)
    score_list = [] 
    l += 1

print(adjustment_cosine_similarity)
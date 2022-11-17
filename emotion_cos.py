# -*- coding: utf-8 -*-
from mlask import MLAsk
import pandas as pd
import demoji
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


emotion_list = ['suki', 'iya', 'none', 'yorokobi', 'aware', 'takaburi', 'yasu', 'kowa', 'ikari', 'haji', 'odoroki']
emotion_count2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# pymlaskの準備
emotion_analyzer = MLAsk()

# データを読み込む
with open('text/review.txt','r',encoding='utf-8') as f:
    text = f.read()
text_1 = demoji.replace(string=text, repl="")  
emotion_a = emotion_analyzer.analyze(text_1)

for k,v in emotion_a['emotion'].items():
    index = emotion_list.index(k)
    emotion_count2[index] += 1

emotion_ave2 = sum(emotion_count2)/11
num2 = 0
for i in emotion_count2:
    emotion_count2[num2] = i - emotion_ave2
    num2 += 1

emo_np2 = np.array([emotion_count2])

df_list = []
movie_name = ['シンゴジラ', 'フォレストガンプ', 'トップガン', 'パラサイト', 'タイタニック',
              'シンウルトラマン', 'ゴッドファーザー', 'ロッキー', 'マイフェアレディ', 'ウエストサイドストーリー',
              'テリファー', 'レプリカズ', 'デイシフト', 'バーフバリ', 'スケートキッチン']
filenames=['dataframe/popular/filmarks_review_godzilla.csv','dataframe/popular/filmarks_review_forrestgump.csv','dataframe/popular/filmarks_review_topgun.csv', 'dataframe/popular/filmarks_review_parasite.csv', 'dataframe/popular/filmarks_review_titanic.csv',
            'dataframe/standard/filmarks_review_ultraman.csv', 'dataframe/standard/filmarks_review_godfather.csv', 'dataframe/standard/filmarks_review_rocky.csv', 'dataframe/standard/filmarks_review_myfairlady.csv', 'dataframe/standard/filmarks_review_westsidestory.csv',
            'dataframe/unpopular/filmarks_review_terrifier.csv', 'dataframe/unpopular/filmarks_review_replicas.csv', 'dataframe/unpopular/filmarks_review_baahubali.csv', 'dataframe/unpopular/filmarks_review_dayshift.csv', 'dataframe/unpopular/filmarks_review_skatekitchen.csv']
for filename in filenames:
    emotion_count1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    df = pd.read_csv(filename, encoding='utf-8', usecols=[1,2]).values.tolist()
    for review in df:
        text = demoji.replace(string=review[0], repl='')
        emotion = emotion_analyzer.analyze(text)
        if emotion['emotion'] is not None:
            #kに感情名、vに対象となった単語が入る。
            for k,v in emotion['emotion'].items():
                index = emotion_list.index(k)
                emotion_count1[index] += len(v) #　複数の単語がある場合、その数だけ感情値としてカウントする。
        else:
            emotion_count1[2] += 1
    emotion_ave1 = sum(emotion_count1)/11
    num1 = 0
    for i in emotion_count1:
        emotion_count1[num1] = i - emotion_ave1
        num1 += 1
    emo_np1 = np.array([emotion_count1])
    #感情値のコサイン類似度を出力
    cs = cosine_similarity(emo_np1, emo_np2)
    df_list.append(cs[0])
df = pd.DataFrame(df_list, index=[movie_name], columns=['ユーザが入力したテキストとの相関係数'])
print(df)


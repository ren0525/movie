# -*- coding: utf-8 -*-
import sys
import codecs
from mlask import MLAsk
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import pandas as pd
import movie_info as mi

# pymlaskの準備
emotion_analyzer = MLAsk()
# タイムゾーンの定義
JST = timezone(timedelta(hours=+9), 'JST')
# カウンターの準備
counter = defaultdict(lambda: defaultdict(int))

# 1. 標準入力でデータを読み込む
df_list = []
df = pd.read_csv(f'dataframe/filmarks_review_{mi.movie_name}.csv', encoding='utf-8', usecols=[1,2]).values.tolist()
for review in df:
	text = review[0]
	date = review[1]
	emotion = emotion_analyzer.analyze(text)
	if emotion['emotion'] is not None:
		for k, v in emotion['emotion'].items():
			counter[date][k] += 1
	else:
		counter[date]['none'] += 1

daily_emotion_list = []
date_list = []
emotion_list = ['suki', 'iya', 'none', 'yorokobi', 'aware', 'takaburi', 'yasu', 'kowa', 'ikari', 'haji', 'odoroki']
date_time = ''
for date in sorted(counter):
	date_time = date
	date_list.append(date)
	emotion_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# 感情成分を頻度順に出力
	for item in sorted(counter[date].items(), key=lambda x: x[1], reverse=True):
		if date_time == date or date_time == '':
			index = emotion_list.index(item[0])
			emotion_count[index] = item[1]
			
	daily_emotion_list.append(emotion_count)

_df = pd.DataFrame(daily_emotion_list, index=pd.Index(data=date_list, name='Date'), columns=emotion_list)
df_list.append(_df)		


# 一つのデータフレームにまとめる
df_emotion = pd.concat(df_list)
print(df_emotion.shape)
df_emotion.head()
df_emotion.to_excel(f'dataframe/filmarks_emotion_{mi.movie_name}.xlsx')
# -*- coding: utf-8 -*-
import sys
import codecs
from mlask import MLAsk
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import pandas as pd

# pymlaskの準備
emotion_analyzer = MLAsk()
# タイムゾーンの定義
JST = timezone(timedelta(hours=+9), 'JST')
# カウンターの準備
counter = defaultdict(lambda: defaultdict(int))

# 1. 標準入力でデータを読み込む
df_list = []
movie_name = 'godzila'
df = pd.read_csv(f'dataframe/filmarks_review_{movie_name}.csv', encoding='utf-8', usecols=[1,2]).values.tolist()
for review in df:
	# 2. データからスレッドタイトルを取り出す
	text = review[0]
	# 3. データから投稿日時を取り出し，年月の情報に変換する
	# UNIX時間をPythonの日付形式に変換（タイムゾーンはJSTを指定）
	# Pythonの日付形式を年月日（YYYY-MM-DD）に変換
	date = review[1]
	# 4. (2)のスレッドタイトルをpymlaskに与え，感情成分を生成する
	emotion = emotion_analyzer.analyze(text)
	if emotion['emotion'] is not None:
		# 5. (3)と(4)の情報をもとに，各感情の日別出現数をカウントアップする
		for k, v in emotion['emotion'].items():
			counter[date][k] += 1
	else:
		# スレッドタイトルに感情を含まない場合はnoneをカウントアップする
		counter[date]['none'] += 1

# 6. (5)のカウント情報をもとに，日別の感情成分を出力する
for date in sorted(counter):
# 感情成分を頻度順に出力
	for item in sorted(counter[date].items(), key=lambda x: x[1], reverse=True):
		_df = pd.DataFrame({item[0]: [item[1]]}, index=[date])
		df_list.append(_df)

# 一つのデータフレームにまとめる
df_review = pd.concat(df_list).reset_index(drop=True)
print(df_review.shape)
df_review.head()

print(df_review)
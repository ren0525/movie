from tf_idf import TfIdf

tf = TfIdf()
tf.add_file('シンゴジラ','text/review_in_godzila.txt')
tf.add_file('シンウルトラマン','text/review_in_ultraman.txt')
tf.create()
print(tf.top_words())
print(tf.word_count())
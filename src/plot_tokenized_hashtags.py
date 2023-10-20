# local imports
import string
import operator

# third party imports
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import pandas as pd
from pprint import pprint
import seaborn as sns

def remove_characters(word):
	characters_to_remove = ['$', '\'', '—'] # add extra characters to remove here
	characters_to_remove += string.punctuation
	for c in characters_to_remove:
		if c in word:
			word = word.replace(c, '')	
	return word

def clean_words(words, words_to_exclude = list()):
	cleaned = list(remove_characters(w.lower())
				for w in words
				if len(w) > 0)
	return list(w for w in cleaned
				if w not in words_to_exclude)

def get_hashtags(body, clean = False):
	hashtags = list(w for w in body.split(' ')
				if len(w) > 2
				and w[0] == '#')

	if clean:
		return clean_words(hashtags)
	else:
		return hashtags

def get_words_in_body(body, include_hashtags = True):
	if include_hashtags:
		words = list(w for w in body.split(' '))
	else:
		words = list(w for w in body.split(' ')
					 if w[0] != '#')

	words_to_exclude = [] # add extra words to remove here
	words_to_exclude += stopwords.words('english')
	return clean_words(words, words_to_exclude)

def tokenize_words(words):
	tokens = dict()
	for w in words:
		if w not in tokens:
			tokens[w] = 1
		else:
			tokens[w] += 1
	return tokens

def plot_barchart_hashtag_count(df):
	sns.set_theme(style = 'whitegrid')
	sns.set(font_scale = 0.75)
	g = sns.barplot(data = df,
					x = 'hashtag', y = 'count',
					color = 'black')
	plt.grid(visible = False)
	plt.xlabel('Word')
	plt.xticks(rotation = 90)
	plt.ylabel('Count')
	plt.title('Top 10 most used hashtags')
	plt.tight_layout()
	plt.savefig('./graphs/most used hashtags_check.png', dpi = 300)

df = pd.read_csv('booktok final.csv')

complete_tokens = dict()

for index, row in df.iterrows():
	hashtags = get_hashtags(str(row['body']))
	tokens = tokenize_words(hashtags)
	for k, v in tokens.items():
		if k in complete_tokens:
			complete_tokens[k] += v
		else:
			complete_tokens[k] = v

df = pd.DataFrame.from_dict(complete_tokens, orient = 'index').reset_index()
df = df.rename({'index': 'hashtag', 0: 'count'}, axis = 'columns')
df = df.sort_values('count', ascending = False)
df = df.head(10)
plot_barchart_hashtag_count(df)
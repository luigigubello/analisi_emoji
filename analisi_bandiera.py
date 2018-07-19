#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from TwitterAPI import TwitterAPI
import numpy as np
import matplotlib.pyplot as plt

# Funzione che controlla se un nickname contiene emoji ita, ma non europa / arcobaleno / bandiera arcobaleno
def check_emoji_ita(word):
	count = False
	emoji_word = ''
	for character in word:
		string = 'U+{:X}'.format(ord(character))
		emoji_word += string
	# Bandiera italiana
	if 'U+1F1EEU+1F1F9' in str(emoji_word):
		count = True
	# Bandiera europea
	if 'U+1F1EAU+1F1FA' in str(emoji_word):
		count = False
	# Arcobaleno
	if 'U+1F308' in str(emoji_word): 
		count = False
	# Bandiera arcobaleno
	if 'U+1F3F3U+FE0FU+200DU+1F308' in str(emoji_word):
		count = False
	return count

# Funzione che controlla se un nickname contiene emoji europa / arcobaleno / bandiera arcobaleno
def check_emoji_other(word):
	count = False
	emoji_word = ''
	for character in word:
		string = 'U+{:X}'.format(ord(character))
		emoji_word += string
	# Bandiera europea
	if 'U+1F1EAU+1F1FA' in str(emoji_word):
		count = True
	# Arcobaleno
	if 'U+1F308' in str(emoji_word): 
		count = True
	# Bandiera arcobaleno
	if 'U+1F3F3U+FE0FU+200DU+1F308' in str(emoji_word):
		count = True
	return count

# Per usare questo script con il tuo account Twitter devi impostare le chiavi delle API Twitter
# Per farlo vai su https://apps.twitter.com/
# Una comoda guida: https://bdthemes.com/support/knowledge-base/generate-api-key-consumer-token-access-key-twitter-oauth/
api = TwitterAPI( \
        consumer_key='####your_key####', \
        consumer_secret='####your_key####', \
        access_token_key='####your_key####', \
        access_token_secret='####your_key####' \
        )

user = input("Digita account: ")

# Cerca gli ultimi 25 tweet scritti dall'account, esclude i retweet e le risposte
number = 25
tweetline = api.request('statuses/user_timeline', {'screen_name': user, 'count' : number, 'exclude_replies' : True, 'include_rts' : False})
venti = len(list(tweetline))
while venti < 25:
	number += 10
	tweetline = api.request('statuses/user_timeline', {'screen_name': user, 'count' : number, 'exclude_replies' : True, 'include_rts' : False})
	venti = len(list(tweetline))
j = 1
grafico_ita = []
grafico_other = []

print("Autore: @{}".format(user))
print("Autore: @{}".format(user), file=open(user + '.txt', 'a'))

for tweet in list(tweetline)[:24]:
	print("")
	print("", file=open(user + '.txt', 'a'))
	print("Tweet ID: {}".format(tweet['id']))
	print("Tweet ID: {}".format(tweet['id']), file=open(user + '.txt', 'a'))
	print("Data: {}".format(tweet['created_at']))
	print("Data: {}".format(tweet['created_at']), file=open(user + '.txt', 'a'))
	print("{}".format(tweet['text']))
	print("{}".format(tweet['text']), file=open(user + '.txt', 'a'))
	print(" -- ")
	print(" -- ", file=open(user + '.txt', 'a'))
	print("Retweetato {} volte".format(tweet['retweet_count']))
	print("Retweetato {} volte".format(tweet['retweet_count']), file=open(user + '.txt', 'a'))

	# Seleziona fino a 100 persone che hanno fatto retweet
	# Poi controlla le emoji presenti nel nickname
	retweets = api.request('statuses/retweets/:%d' % tweet['id'], {'count' : 100})
	i = 0
	flag_ita = 0
	flag_other = 0
	for retweet in retweets:
		if check_emoji_ita(retweet['user']['name']) == True:
			flag_ita += 1
		if check_emoji_other(retweet['user']['name']) == True:
			flag_other += 1
		i += 1
	print("Retweet analizzati: {}".format(i))
	print("Retweet analizzati: {}".format(i), file=open(user + '.txt', 'a'))
	if i > 0:
		print("User con emoji bandiera italiana trovati: {}".format(flag_ita))
		print("User con emoji bandiera italiana trovati: {}".format(flag_ita), file=open(user + '.txt', 'a'))
		percentuale_ita = flag_ita/i*100
		print("Percenutale di emoji bandiera italiana user casuali: {}%".format(int(percentuale_ita)))
		print("Percenutale di emoji bandiera italiana user casuali: {}%".format(int(percentuale_ita)), file=open(user + '.txt', 'a'))
		grafico_ita.append(int(percentuale_ita))
		print("User con emoji bandiera europea / arcobaleno trovati: {}".format(flag_other))
		print("User con emoji bandiera europea / arcobaleno trovati: {}".format(flag_other), file=open(user + '.txt', 'a'))
		percentuale_other = flag_other/i*100
		print("Percenutale di emoji bandiera europea / arcobaleno user casuali: {}%".format(int(percentuale_other)))
		print("Percenutale di emoji bandiera europea / arcobaleno user casuali: {}%".format(int(percentuale_other)), file=open(user + '.txt', 'a'))
		grafico_other.append(int(percentuale_other))
	else:
		print("Nessun retweet trovato.")
		print("Nessun retweet trovato.", file=open(user + '.txt', 'a'))
		grafico_ita.append(0)
		grafico_other.append(0)
	print("")
	j += 1
print("Tweet originali: {}".format(j))
print("Tweet originali: {}".format(j), file=open(user + '.txt', 'a'))
print("Media emoji bandiera italiana: {}".format(np.mean(grafico_ita)))
print("Media emoji bandiera italiana: {}".format(np.mean(grafico_ita)), file=open(user + '.txt', 'a'))
print("Varianza emoji bandiera italiana: {}".format(np.var(grafico_ita)))
print("Varianza emoji bandiera italiana: {}".format(np.var(grafico_ita)), file=open(user + '.txt', 'a'))
print("Media emoji bandiera europea / arcobaleno: {}".format(np.mean(grafico_other)))
print("Media emoji bandiera europea / arcobaleno: {}".format(np.mean(grafico_other)), file=open(user + '.txt', 'a'))
print("Varianza emoji bandiera europea / arcobaleno: {}".format(np.var(grafico_other)))
print("Varianza emoji bandiera europea / arcobaleno: {}".format(np.var(grafico_other)), file=open(user + '.txt', 'a'))

# Crea un grafico a barre
# Grazie: https://python-graph-gallery.com/4-add-title-and-axis-label/
def crea_grafico(array, titolo):
	valori_y = array
	valori_x = array
	y_pos = np.arange(len(valori_x))
	plt.bar(y_pos, valori_y, color = (0.5,0.1,0.5,0.6))
	plt.title('Account: @' + user)
	plt.ylim(0,100)
	plt.xticks(y_pos, valori_x)
	plt.savefig(user + '_' + titolo + '_plot.png')
	plt.close()

titolo = 'ita'
crea_grafico(grafico_ita, titolo)
titolo = 'other'
crea_grafico(grafico_other, titolo)

from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

df = pd.read_json('article.json')
df = df.drop_duplicates()
df_dict = df.to_dict()

authors = df['Authors'].to_list()

authors_data = []
art_authors = []
qt_authors = []

for a in authors:
    art_authors.append(a.split(','))
    for b in a.split(','):
        authors_data.append(b.strip().capitalize())

for a in art_authors:
    qt_authors.append(len(a))

list_author = (Counter(authors_data))

occurrences = list(list_author.values())
name_authors = list(list_author.keys())

qt_authors.sort()

tags = df['Tags'].to_list()

tags_data = []
art_tags = []
qt_tags = []

for a in tags:
    art_tags.append(re.split(',|;|\.',a.strip()))
    for b in re.split(',|;|\.', a.strip()):
        if b != "Tags not found" and b != "":
            tags_data.append(b.strip().capitalize().strip())

for a in art_tags:
    qt_tags.append(len(a))

list_tags = (Counter(tags_data))

occurrences = list(list_tags.values())
name_authors = list(list_tags.keys())

dates = df['Date'].to_list()

date_data = []

for a in dates:
    date_data.append(a)

date_dict = (Counter(date_data))


#Quantidade de Artigos por Ano

#fig, ax = plt.subplots()
#line1, = ax.plot(date_dict.values(), label='Keys', linestyle='--')

plt.plot(date_dict.keys(), date_dict.values(), 'o--')
plt.xlabel('Anos')
plt.ylabel('Artigos')
plt.title('Quantidade de Artigos por Ano')
plt.grid(True)
plt.show()


#for i in df_dict['Date']:
    #print(df_dict['Authors'][i])

#print(df_dict['Date'].values())

inverted_df_dict = dict()

for key in df_dict['Date']:
    value = df_dict['Date'][key]
    #print(value)
    inverted_df_dict[value] = key

#print(df_dict['Date'])
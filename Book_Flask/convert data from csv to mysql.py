#!/usr/bin/env python
# coding: utf-8

# In[634]:

#
# convert data from csv (goodbooks-10k from kaggle) to sql alchemy by dataframe python 3
# using jupyter notebook

import pandas as pd
import sqlalchemy
import os

URI = 'mysql+mysqlconnector://' + os.environ.get('MYSQL_USER') + ':' + os.environ.get('MYSQL_PASSWORD') + '@localhost/' + os.environ.get('MYSQL_DB')
connection = sqlalchemy.create_engine(URI)

df = pd.read_csv('books.csv')
df = df[['book_id', 'original_title', 'isbn','isbn13','authors', 'original_publication_year','image_url', 'average_rating', 'books_count']]


# In[635]:


df.sort_values(inplace=True, by = ['book_id'])


# In[636]:


data = [{'GenreID': 1, 'Name': 'Science fiction'},
       {'GenreID': 2, 'Name': 'Satire'},
       {'GenreID': 3, 'Name': 'Drama'},
       {'GenreID': 4, 'Name': 'Romance'},
       {'GenreID': 5, 'Name': 'Mystery'},
       {'GenreID': 6, 'Name': 'Horror'},
       {'GenreID': 7, 'Name': 'Self help'},
       {'GenreID': 8, 'Name': 'Health'},
       {'GenreID': 9, 'Name': 'Guide'},
       {'GenreID': 10, 'Name': 'Travel'},
       {'GenreID': 11, 'Name': 'Religion, Spirituality & New Age'},
       {'GenreID': 12, 'Name': 'Science'},
       {'GenreID': 13, 'Name': 'History'},
       {'GenreID': 14, 'Name': 'Math'},
       {'GenreID': 15, 'Name': 'Anthology'},
       {'GenreID': 16, 'Name': 'Poetry'},
       {'GenreID': 17, 'Name': 'Encyclopedias'},
       {'GenreID': 18, 'Name': 'Dictionaries'},
       {'GenreID': 19, 'Name': 'Comics'},
       {'GenreID': 20, 'Name': 'Cookbooks'},
       {'GenreID': 21, 'Name': 'Diaries'},
       {'GenreID': 22, 'Name': 'Journals'},
       {'GenreID': 23, 'Name': 'Prayer books'},
       {'GenreID': 24, 'Name': 'Series'},
       {'GenreID': 25, 'Name': 'Trilogy'},
       {'GenreID': 26, 'Name': 'Biographies'},
       {'GenreID': 27, 'Name': 'Autobiographies'},
       {'GenreID': 28, 'Name': 'Fantasy'},
       {'GenreID': 29, 'Name': 'Others'}]


# In[637]:


data_genres = pd.DataFrame(data)


# In[638]:


authors_name = []

authors_id = []
for i in range(len(authors)):
    authors_id.append(i+1)


# In[639]:


for i in range(len(df['book_id']) - 1):
    for x in (df.iloc[i]['authors']).split(','):
        temp = x.strip()
        if temp not in authors_name:
            authors_name.append(temp)


# In[640]:


data_authors = pd.DataFrame({'AuthorID': authors_id, 'Name': authors})


# In[641]:


a = data_authors[data_authors['Name'] == 'J.K. Rowling'].values[0].tolist()
a[1]


# In[642]:


def get_id_of_author(s):
    temp = data_authors[data_authors['Name'] == s].values[0].tolist()
    return temp[0]


# In[643]:


def replace_author(s):
    authors_id = ''
    for word in s.split(','):
        stripped_word = word.strip()
        if stripped_word in authors:
            if authors_id != '':
                authors_id += ', ' + str(get_id_of_author(stripped_word))
            authors_id += str(get_id_of_author(stripped_word))
    return authors_id       


# In[644]:


replace_author('J.K. Rowling, Mary GrandPré, Rufus Beck')


# In[645]:


temp = []
for x in range(len(df['book_id'])):
    temp.append(df.iloc[x]['authors'])


# In[646]:


own = []
for i in temp:
    own.append(replace_author(i))


# In[647]:


df['authors'] = own


# In[648]:


import random
random_genre = []
for i in range(len(df['book_id'])):
    random_genre.append(random.randint(1, len(data)))
random_price = []
for i in range(len(df['book_id'])):
    random_price.append(random.randint(5, 500))


# In[649]:


df['GenreID'] = random_genre
df['Price'] = random_price


# In[650]:


df.rename(columns = {'authors' : 'AuthorsID',
                     'book_id' : 'BookID',
                     'original_title' : 'Title',
                     'isbn' : 'ISBN',
                     'isbn13' : 'ISBN13',
                     'original_publication_year' : 'PublicationYear',
                     'image_url' : 'ImgUrl',
                     'average_rating': 'AvgRating',
                     'books_count' : 'Quantity'}, inplace = True)


# In[651]:


df.columns = ['BookID', 'Title', 'ISBN', 'ISBN13', 'AuthorsID', 'PublicationYear', 'ImgUrl', 'Price', 'AvgRating', 'Quantity', 'GenreID']


# In[653]:


data_authors.set_index('AuthorID', inplace = True)

data_authors.to_sql(con = connection, name = 'author', if_exists = 'append')


# In[654]:


data_genres.set_index('GenreID', inplace = True)

data_genres.to_sql(con = connection, name = 'genre', if_exists='append')


# In[655]:


BookID = df['BookID'].values.tolist()
Title = df['Title'].values.tolist()
ISBN = df['ISBN'].values.tolist()
ISBN13 = df['ISBN13'].values.tolist()
AuthorsID = df['AuthorsID'].values.tolist()
PublicationYear = df['PublicationYear'].values.tolist()
ImgUrl = df['ImgUrl'].values.tolist()
Price = df['Price'].values.tolist()
AvgRating = df['AvgRating'].values.tolist()
Quantity = df['Quantity'].values.tolist()
GenreID = df['GenreID'].values.tolist()


# In[656]:


book = pd.DataFrame({'BookID':BookID})
book['Title'] = Title
book['ISBN'] = ISBN
book['ISBN13'] = ISBN13
book['AuthorsID'] = AuthorsID
book['PublicationYear'] = PublicationYear
book['ImgUrl'] = ImgUrl
book['Price'] = Price
book['AvgRating'] = AvgRating
book['Quantity'] = Quantity
book['GenreID'] = GenreID


# In[657]:


book.set_index('BookID', inplace = True)

book.to_sql(con = connection, name = 'book', if_exists='append')


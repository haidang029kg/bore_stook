#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sqlalchemy
import os
import random


# In[2]:


URI = LOCAL_URI = 'mysql+pymysql://flask:Flask_123@127.0.0.1:3306/borestook'
connection = sqlalchemy.create_engine(URI)


# In[3]:


os.environ.get('MYSQL_DB')
os.environ.get('MYSQL_USER')


# In[4]:


df = pd.read_csv('books.csv')
df = df[['book_id', 'original_title', 'isbn','authors', 'original_publication_year','image_url', 'average_rating', 'books_count']]
df.sort_values(inplace=True, by = ['book_id'])


# In[5]:


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


# In[6]:


data_genres = pd.DataFrame(data)


# In[7]:


authors_name = []

for i in range(len(df['book_id']) - 1):
    for x in (df.iloc[i]['authors']).split(','):
        temp = x.strip()
        if temp not in authors_name:
            authors_name.append(temp)

authors_id = []
for i in range(len(authors_name)):
    authors_id.append(i+1)


# In[8]:


data_authors = pd.DataFrame({'AuthorID': authors_id, 'Name': authors_name})


# In[9]:


a = data_authors[data_authors['Name'] == 'J.K. Rowling'].values[0].tolist()
a[1]


# In[10]:


def get_id_of_author(s):
    temp = data_authors[data_authors['Name'] == s].values[0].tolist()
    return temp[0]


# In[11]:


def replace_author(s):
    authors_id = ''
    for word in s.split(','):
        stripped_word = word.strip()
        if stripped_word in authors_name:
            if authors_id != '':
                authors_id += ', ' + str(get_id_of_author(stripped_word))
            authors_id += str(get_id_of_author(stripped_word))
    return authors_id       


# In[12]:


replace_author('J.K. Rowling, Mary GrandPré, Rufus Beck')


# In[13]:


temp = []
for x in range(len(df['book_id'])):
    temp.append(df.iloc[x]['authors'])


# In[14]:


own = []
for i in temp:
    own.append(replace_author(i))


# In[15]:


df['authors'] = own


# In[16]:


random_genre = []
random_price = []
for i in range(len(df['book_id'])):
    random_genre.append(random.randint(1, len(data)))

for i in range(len(df['book_id'])):
    random_price.append(random.randint(5, 500))


# In[17]:


df['GenreID'] = random_genre
df['Price'] = random_price


# In[18]:


df.rename(columns = {'authors' : 'AuthorsID',
                     'book_id' : 'BookID',
                     'original_title' : 'Title',
                     'isbn' : 'ISBN',
                     'original_publication_year' : 'PublicationYear',
                     'image_url' : 'ImgUrl',
                     'average_rating': 'AvgRating',
                     'books_count' : 'Quantity'}, inplace = True)


# In[19]:


df = df[['BookID', 'Title', 'ISBN', 'AuthorsID', 'PublicationYear', 'ImgUrl', 'Price', 'AvgRating', 'Quantity', 'GenreID']]


# In[20]:


data_authors.set_index('AuthorID', inplace = True)


# In[21]:


data_authors.to_sql(con = connection, name = 'author', if_exists = 'append')


# In[22]:


data_genres.set_index('GenreID', inplace = True)

data_genres.to_sql(con = connection, name = 'genre', if_exists='append')


# In[23]:


BookID = df['BookID'].values.tolist()
Title = df['Title'].values.tolist()
ISBN = df['ISBN'].values.tolist()
AuthorsID = df['AuthorsID'].values.tolist()
PublicationYear = df['PublicationYear'].values.tolist()
ImgUrl = df['ImgUrl'].values.tolist()
Price = df['Price'].values.tolist()
AvgRating = df['AvgRating'].values.tolist()
Quantity = df['Quantity'].values.tolist()
GenreID = df['GenreID'].values.tolist()


# In[24]:


book = pd.DataFrame({'BookID':BookID})
book['Title'] = Title
book['ISBN'] = ISBN
book['AuthorsID'] = AuthorsID
book['PublicationYear'] = PublicationYear
book['ImgUrl'] = ImgUrl
book['Price'] = Price
book['AvgRating'] = AvgRating
book['Quantity'] = Quantity
book['GenreID'] = GenreID


# In[25]:


book['Title'].fillna('Unkown', inplace = True)


# In[26]:


book.set_index('BookID', inplace = True)


# In[27]:


book.to_sql(con = connection, name = 'book', if_exists='append')


# 

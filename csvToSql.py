#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sqlalchemy
import os
import random

URI = 'mysql+pymysql://flask:Flask_123@127.0.0.1:3306/borestook'
connection = sqlalchemy.create_engine(URI)

df = pd.read_csv('books.csv')
df = df[['book_id', 'original_title', 'isbn','authors', 'original_publication_year','image_url', 'average_rating', 'books_count']]
df.sort_values(inplace=True, by = ['book_id'])


# In[2]:


#Clean database
rrrasdfasdf
db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
db.drop_all()
db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
db.create_all()


# In[3]:


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


# In[4]:


data_genres = pd.DataFrame(data)


# In[5]:


authors_name = []

for i in range(len(df['book_id']) - 1):
    for x in (df.iloc[i]['authors']).split(','):
        temp = x.strip()
        if temp not in authors_name:
            authors_name.append(temp)

authors_id = []
for i in range(len(authors_name)):
    authors_id.append(i+1)


# In[6]:


data_authors = pd.DataFrame({'AuthorID': authors_id, 'Name': authors_name})


# In[7]:


a = data_authors[data_authors['Name'] == 'J.K. Rowling'].values[0].tolist()
a[1]


# In[8]:


def get_id_of_author(s):
    temp = data_authors[data_authors['Name'] == s].values[0].tolist()
    return temp[0]


# In[9]:


get_id_of_author('Frank Herbert')


# In[10]:


def replace_author(s):
    authors_id = ''
    for word in s.split(','):
        stripped_word = word.strip()
        if stripped_word in authors_name:
            if authors_id != '':
                authors_id += (',' + str(get_id_of_author(stripped_word)))
            else:
                authors_id += str(get_id_of_author(stripped_word))
    return authors_id


# In[11]:


replace_author('Heidi Murkoff, Sharon Mazel, Heidi Murkoff, Arlene Eisenberg, Sandee Hathaway, Mark D. Widome')


# In[12]:


temp = []
for x in range(len(df['book_id'])):
    temp.append(df.iloc[x]['authors'])


# In[13]:


own = []
for i in temp:
    own.append(replace_author(i))


# In[14]:


df['authors'] = own


# In[15]:


random_genre = []
random_price = []
for i in range(len(df['book_id'])):
    random_genre.append(random.randint(1, len(data)))

for i in range(len(df['book_id'])):
    temp_price = round(random.uniform(1.00, 10.00), 2)
    random_price.append(temp_price)


# In[16]:


df['GenreID'] = random_genre
df['Price'] = random_price


# In[17]:


df.rename(columns = {'authors' : 'AuthorsID',
                     'book_id' : 'BookID',
                     'original_title' : 'Title',
                     'isbn' : 'ISBN',
                     'original_publication_year' : 'PublicationYear',
                     'image_url' : 'ImgUrl',
                     'average_rating': 'AvgRating',
                     'books_count' : 'Quantity'}, inplace = True)


# In[18]:


df = df[['BookID', 'Title', 'ISBN', 'AuthorsID', 'PublicationYear', 'ImgUrl', 'Price', 'AvgRating', 'Quantity', 'GenreID']]


# In[19]:


#delete book with no image
df = df[df.ImgUrl != 'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png']
#delete book with no title
df = df[df.Title != ' ']


# In[20]:


data_authors.set_index('AuthorID', inplace = True)

data_authors.to_sql(con = connection, name = 'author', if_exists = 'append')


# In[21]:


data_genres.set_index('GenreID', inplace = True)

data_genres.to_sql(con = connection, name = 'genre', if_exists='append')


# In[22]:


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


# In[23]:


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


# In[24]:


book['Title'].fillna('Unkown', inplace = True)


# In[25]:


book.set_index('BookID', inplace = True)


# In[26]:


book.to_sql(con = connection, name = 'book', if_exists='append')


# In[27]:


data_IsPaid = [{'IsPaidID' : 1, 'NamePaid' : 'No'},
              {'IsPaidID' : 2, 'NamePaid' : 'Yes'}]
data_IsPaid = pd.DataFrame(data_IsPaid)
data_IsPaid.set_index('IsPaidID', inplace = True)
data_IsPaid.to_sql(con = connection, name = 'ispaid', if_exists='append')

data_Status = [{'StatusID' : 1, 'NameStatus' : 'Waiting'},
              {'StatusID' : 2, 'NameStatus' : 'Packaging'},
              {'StatusID' : 3, 'NameStatus' : 'Delivering'},
              {'StatusID' : 4, 'NameStatus' : 'Delivered'},
              {'StatusID' : 5, 'NameStatus' : 'Rejected'}]
data_Status = pd.DataFrame(data_Status)
data_Status.set_index('StatusID', inplace = True)
data_Status.to_sql(con = connection, name = 'status', if_exists='append')

data_PaymentMethod = [{'PaymentMethodID' : 1, 'NamePayment' : 'Credit Card'},
                     {'PaymentMethodID' : 2, 'NamePayment' : 'Cash'},
                     {'PaymentMethodID' : 3, 'NamePayment' : 'Bank Transfer'},
                     {'PaymentMethodID' : 4, 'NamePayment' : 'Code'}]
data_PaymentMethod = pd.DataFrame(data_PaymentMethod)
data_PaymentMethod.set_index('PaymentMethodID', inplace = True)
data_PaymentMethod.to_sql(con = connection, name = 'paymentmethod', if_exists='append')


# In[28]:


from Book_Flask import bcrypt
hashed_passwowrd_admin = bcrypt.generate_password_hash('admin').decode('utf-8')
hashed_passwowrd_admin


# In[29]:


string = "insert into user (FirstName, LastName, Phone, Email, ImgUrl, Password, RoleAdmin) values ('Dang', 'Vu', '0364292129', 'vnhd1995@gmail.com', 'default.jpg', '$2b$12$TFSOyCw1scepsmVighyUyOHFdgOqwv5/E7fyCNxAuNF0wwnQLPOSe', True);"
db.session.execute(string)
db.session.commit()


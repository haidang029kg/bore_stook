#!/usr/bin/env python
# coding: utf-8

# In[95]:


from goodreads import client
import pandas as pd
import re


# In[96]:


gc = client.GoodreadsClient('mRdp5MMam7y3J97qNeLElw','16GgrrTdkm5fA9ooWzqVTTc8nkpvh4HqWjtQI8rIA')


# In[97]:


books = pd.read_csv('~/Downloads/goodbooks-10k/books.csv')


# In[98]:


book_id = books.book_id


# In[99]:


bookDes = pd.DataFrame(columns=['book_id','title','description'])


# In[100]:


book_id_error = []


# In[101]:


def remove_tagg(s):
    return re.sub(r'\<.*?\>',r'', s)


# In[102]:


for i in range(0, len(book_id) - 1): #len(book_id) - 1
    print (i, ' Book ID: ',book_id[i])
    try:
        book = gc.book(book_id[i])
        des = remove_tagg(book.description)
        bookDes.loc[i] = [book_id[i],book.title, des]
        print('success')
    except:
        bookDes.loc[i] = [book_id[i],'error','error']
        print('error')
        book_id_error.append(book_id[i])


# In[103]:


bookDes.set_index('book_id', inplace = True)
bookDes.to_csv('result_crawl_description.csv')


# In[105]:


error_books = pd.DataFrame(book_id_error, columns = ['id'])
error_books.set_index('id', inplace = True)

error_books.to_csv('result_error_crawl_description.csv')


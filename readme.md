#How to run
1. install essential packages from requirements.txt
2. Fill in missing fields in env.sh
3. Run `chmod u+x env.sh`
4. Run `./env.sh`

5. Crawl book description by running 'crawlBookDescriotion.py'

6. Import data from csv to mysql
    - replace parameters in file "convert data from csv to mysql.py"
        parameters: 
			+ path of csv file (book.csv)
			+ path of csv file (result_crawl_description.csv) 
				takes approximately 5 hours for crawling or can use the exist csv file (result_crawl_description) crawled in advance
			+ path of "db" variable (instance for SQLAlchemy) in SOURCE CODE
    - in file models.db in SOURCE CODE, switch rows to become comment rows where rows contain "db" variable
    to avoid using variable error when it has not created yet

    - run "csvToSql.py"
    - uncomment rows changed above

7. run file "main.py" with python 3.6



--------Contact-----------
Vu Nguyen Hai Dang
Phone: 0364292129
Email: vnhd1995@gmail.com

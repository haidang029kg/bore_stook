1. install essential packages from requirements.txt
2. create database, secret key, email for project and export information created to bash file (linux OS)
    should replace by your own email avoiding google account security
    export these by terminal:


        export MYSQL_HOST=localhost
        export MYSQL_USER=flask
        export MYSQL_PASSWORD=Flask_123
        export MYSQL_DB=borestook
        export SECRET_KEY=1356d24c50414b44221cbc80ac0bf45a
        export MAIL_USERNAME=vuttan1995@gmail.com
        export MAIL_PASSWORD=01664292129
        export CLOUD_SQL_INSTANCES=final-thesis-100496:asia-east2:borestook



3. convert data from csv to mysql
    - replace parameters in file "convert data from csv to mysqql.py"
        parameters: + path of csv file (book.csv)
                    + path of "db" variable (instance for SQLAlchemy) in SOURCE CODE
    - in file models.db in SOURCE CODE, switch rows to become comment rows where rows contain "db" variable
    to avoid using variable error when it has not created yet

    - run "convert data from csv to mysql.py"



--------Contact-----------
Vu Nguyen Hai Dang
Phone: 0364292129
Email: vnhd1995@gmail.com
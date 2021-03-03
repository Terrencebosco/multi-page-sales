# multi-page-sales

## First multi page dashboard
---
run application:
`https://tb-dash.herokuapp.com/` : single page dash

`https://tb-mdash.herokuapp.com/` :multiple page

### tools that helped:
* https://dash-bootstrap-components.opensource.faculty.ai/docs
* https://github.com/facultyai/dash-bootstrap-components/tree/master/examples
* https://dash.plotly.com/urls
* https://www.youtube.com/watch?v=RMBSQ6leonU&ab_channel=CharmingData

# sales_analysis

## Application Link:

[link to application](https://tb-dash.herokuapp.com/)

`https://tb-dash.herokuapp.com/`

started work with sales data.

converted sql fiel to sqlite for ease of access with python. (better way?). installed and played with mysql via command line.

---

mysql locally: [helped](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04), [doc](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

command line -> sudo mysql

to access local sql dump file:

mysql > CREATE DATABASE >name<

mysql > use >name<

mysql > source /filepath/>name<.sql

---

to convert sql to sqlite3 for ease of use: [converter](https://github.com/Terrencebosco/mysql2sqlite)


cd -> utilites/mysql2sqlite

terminal -> ./mysql2sqlite dump_mysql.sql | sqlite3 mysqlite3.db

---

created fucntion that converts sql tables to panda dataframes then stores those dataframes in a dictionary to ease of access.

add conda env to kernal `python -m ipykernel install --user --name <name of env?> --display-name "<name of kernal>"`

---

## created web application with heroku.

[documentation](https://dash.plotly.com/)

to get it running i ran into several errors. one being a time out error but the command `git config http.postBuffer 524288000`

another error was the pathing from the procfile to the application. ( i didnt use create_app() this time, maybe that was my problem?)

pushing to heroku as follows:

    heroku create -n name

    git init

    git add .

    git commit -m "comment"

    git push origin main

    git push heroku main

also created allies script to add commi and push to with git `git cmp "comment"`


```
docker build -t <image name>:latest .

docker run -it <image name>

docker stop <container id>

run flask app from local container:
    docker run -d -p 5000:5000 <image name>
make new app and push image to heroku:

heroku create <app name>

heroku container:push web --app <app name>

heroku container:release web --app <app name>
can update image with

heroku container:push web --app <app name>

heroku container:release web --app <app name>
```



TODO:
- ~~merge all data~~
- EDA
    - company data
    - month
    - year

- Visual
- ~~plotyl dash?~~
- look into making plots by yearly distrobution
- pages by type
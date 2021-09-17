# Meet CS Project
### Description
This is my meet  y2 CS TA project, it covers all of the requirements except the bonus level 3 (i didnt know how to implement 
them into this specific project) it uses a database to save all of the user credentials.
### Build Instructions
- First install the packages required to run the Flask server:
```shell script
pip3 install -r requirements.txt
```
- Run the server:
```shell script
python app.py
```
- Go to your browser to address: `http://127.0.0.1:5000/` (you can see the address
after running the previous command)

### Notes
- to check what is stored in the database, normal sqlite commands can be used
such as
```shell script
sqlite3 database.db
select * from user;
```
this will show you what is in the database in a `id|username|email|password` pattern.
- The user credentials are CASE SENSITIVE and the username is unique.
- the city name HAS to be grammatically correct or else it wont work.
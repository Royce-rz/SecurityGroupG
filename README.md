# ELEC00138 Group G 
## Web APP
The main web app is **`web/my_app.py`**, this file include all of the system built and the security for attack is on. You need to register a acounnt then login with this valid account, then you can access our user data.
#### The SQL database is supposed to resume once the app request it, so the SQL database would show unavailabe at first time running. The database would resume within one minute, try to restart the web app after one minutes.
## Attack - unsafe APP
**`web/unsafe_app.py`** shows the app without any protect, you can attack the website by generate this file.
### brute force attack
You get the username and password by running **`web/brute_force_attack`**.py.
### SQL injection
After you login with the username and password got by brute force attack, you can do SQL injection in User Data page.
In the search box, enter **` 1'; delete from users where username='Test `** to delete user with unauthorzied SQL command or **` 1'; update users set Illness='healthy' where username='Test `** to change user's data.


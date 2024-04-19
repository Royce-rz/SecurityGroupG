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
### IoT devices system
In this project, an Arduino MKRWIFI1010 is used as the main microcontroller and ICM20948 is used as the inertial sensor to simulate a smart hospital scenario for collecting patient motion data. A local Flask server with HTTPS protocol is built to receive the data from the microcontroller wirelessly. 
In this project, we used a self-signed certificate, so we need to generate a separate certificate for each domain name. The key in the project uses the IP address in the WiFi network under the test environment as the domain name, so it needs to be regenerated to enable the HTTPS function when reproducing.
Run *`arduino.ino`* and *`security_cw_localhost.py`* can simulate the unencrypted process through HTTP transmission. 
Run *`arduino_encrption.ino`* and *`security_cw_localhost_encrp.py`* can simulate the encryption process. 
The data output could be found in the CSV file. 

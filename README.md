# Weavedin

Steps to run
pip install -r requirements.txt

Go to mysql console and execute below commands
CREATE DATABASE JaffaData;
CREATE USER 'jaffa'@'localhost' IDENTIFIED BY 'jaffa';
GRANT ALL PRIVILEGES ON *.* TO 'jaffa'@'localhost';

Now run
python run.py

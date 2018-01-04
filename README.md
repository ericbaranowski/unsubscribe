# unsubscribe.robot

See http://unsubscriberobot.com

Build and run the unsubscribe robot using the commands.sh file. There are three docker files for different tasks. 

Dockerfile is the master. It reads emails from gmail and processes them with the simulated browser.

Dockerfile_slave is a second process to just process entries in the database. It constantly runs the simulated browser. The browser takes most of the processing and time, and we don't want to read from gmail in a conflicting way.

Dockerfile_analytics gives some high level metrics on users and success rate.

Your directory structure should be:

auth/
unsubscribe/ (this repo)
Dockerfile (duplicated from the unsubscribe dir)

This way we keep the auth files outside of the repo and don't have to worry about gitignore. The auth directory contains two files:

sql.txt
sql_user
sql_pass
ip_address

gmail.txt
gmail_address
gmail_password
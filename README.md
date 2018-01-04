# unsubscribe.robot

http://unsubscriberobot.com

Build and run the unsubscribe robot using the commands.sh file. There are three docker files for different tasks. 

1. Dockerfile is the master. It reads emails from gmail and processes them with the simulated browser.
1. Dockerfile_slave is a second process to just process entries in the database. It constantly runs the simulated browser. The browser takes most of the processing and time, and we don't want to read from gmail in a conflicting way.
1. Dockerfile_analytics gives some high level metrics on users and success rate.

Your directory structure should be:

auth/<br/>
unsubscribe/ (this repo)<br/>
Dockerfile (duplicated from the unsubscribe dir)<br/>

This way we keep the auth files outside of the repo and don't have to worry about gitignore. The auth directory contains two files:

sql.txt<br/>
sql_user<br/>
sql_pass<br/>
ip_address<br/>

gmail.txt<br/>
gmail_address<br/>
gmail_password<br/>
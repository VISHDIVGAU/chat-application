# chat-application
Flash web framework for Front end
Grpc and Rest API for backend
MongoDB for DataBase

Instruction to run the application-:
System requirements-:
• Linux operating system
• Python 3.9 version
• Mongo DB locally installed (refer website
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/ for installation
instructions)
• Sudo mkdir –p /data/db
• sudo chmod 0755 /data/db && sudo chown $USER /data/db
• Ssh localhost
• Start mongo db daemon

1. Install python and mongo dB server on your local machine.
2. Create a virtual environment.
python3 -m venv chatApplication
$source chatApplication/bin/activate
3. Unzip chatApp.
4. Pip3 install requirements.txt
5. Start grpc server.
python3 server.py
6. Start flask app server
Python3 app.py
7. In web browser open http://127.0.0.1:5000.
8. You will be redirected to login page. Click three bars on the nav bar to register.
9. Create two or three users.
10. Login with different user details in two different browsers.
11. You will see list of registered users.
12. Click on the other users you have logged in different browser.
13. You will see chat window open up.
14. Do the same thing with the other user.
15. Check the two chat windows and see if they are able to send and receive messsages.

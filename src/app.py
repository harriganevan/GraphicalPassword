from flask import Flask, redirect
import views
import os
import db
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__) #creating flask app

#run this while in the src folder
#doesnt need to be run if instance folder already exists
#creates a instance path - holds database file
# try:
#     os.makedirs(app.instance_path)
# except OSError:
    # pass

#setting up mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'graphicalpws@gmail.com' #hide these
app.config['MAIL_PASSWORD'] =  'ohkwlxcgggvhepwn' #HIDE THIS
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#add secret key and path to database file to the app config
app.config.update(
        SECRET_KEY='481ca7d24ccdf2c0fb90995f87ac062bbb087b65588a7b42', #ideally move this to a config file - do not publish this
        DATABASE=os.path.join(app.instance_path, 'app.sqlite')
)

db.init_app(app) #create initialization command

app.register_blueprint(views.views, url_prefix="/") #register blueprints from views.py

if __name__ == '__main__':
    app.run(debug=True)


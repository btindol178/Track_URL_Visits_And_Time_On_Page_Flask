from flask import Flask,render_template,session,request,jsonify 
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'sdflksjslksajfsda' # NOT KOSSURE BUT FOR NOW

db = SQLAlchemy(app)

# Create tables at first
@app.before_first_request
def create_tables():
    db.create_all() 


class LogForm(FlaskForm):
    firstname = StringField('Whats your?', validators=[DataRequired()])
    lastname = StringField('Whats your?', validators=[DataRequired()])
    email = StringField('Whats your?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# To log the form data and how long the user was on the page
class LogData(db.Model):
    __tablename__ = 'logdata'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    starttime = db.Column(db.String(120), unique=True)
    endtime = db.Column(db.String(120), unique=True)


    def __init__(self, firstname, lastname, email,starttime,endtime):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.starttime = starttime
        self.endtime = endtime
  

# to count how many visits the user visited on 
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    page = db.Column(db.String(100))

    def __init__(self):
        self.count = 0

# turn this into calss and import to record who is logged in to the session aka. user then take log data and make relationship to tables
# HOW MANY TIMES USER VISITED THE VISIT PAGE!!! 
@app.route("/visit")
def hello():
    v = Visit.query.first()
    print(v)
    if not v:
        v = Visit()
        v.count += 1
        v.page = "visit"
        db.session.add(v)
    v.count +=1
    db.session.commit()
    return jsonify(counter=v.count,page = v.page)


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
   
    form = LogForm()

    if request.method == 'POST':     # OR if form.validate_on_submit():
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        click = request.args.get('clicks')

        print(firstname)
        print(lastname)
        print(email)
        print(click)
  

        # This will input start time on page and end time on page 
        entry = LogData(firstname=firstname, lastname=lastname, email = email,
                        starttime=session.pop('start_time', None), endtime=datetime.utcnow())
                        #difference = later_time - first_time
        db.session.add(entry)
        db.session.commit()

        #return render_template("success.html")
        return render_template('index.html', form=form)
    session['start_time'] = datetime.utcnow()

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
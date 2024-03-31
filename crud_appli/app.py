from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Sam@4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def Index():
    alldata = Data.query.all()
    return render_template("index.html", employes=alldata)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['mail']
        phone = request.form['phn']

        mydata = Data(name, email, phone)
        db.session.add(mydata)  # Corrected line
        db.session.commit()

        flash("employee added sussesfully")
        return redirect(url_for('Index'))

@app.route('/update',methods=['POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])  # Added square brackets around 'GET', 'POST'
def delete(id):
    my_data = Data.query.get(id)  # Added missing '=' sign
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('Index'))



if __name__ == "__main__":
    app.run(debug=True)

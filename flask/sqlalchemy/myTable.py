# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# sqlite url formats are 'sqlite:///relative path' or 'sqlite://// absolute path'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xxx.db'
# Connect db to the app
db = SQLAlchemy(app)

class BlogPost(db.Model):
    # Add columns as variables with db.Column() method
    # To assign the datatype, use db.Interger/db.String/db.Datetime/db.Text
    # And other arrtibutes like primary_key=T/F, nullable=T/F, default=
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    # datetime.utcnow() is a current timestamp value
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    # This function will give every data a name which will be shown when you query it
    def __repr__(self):
        return 'BlogPost ' + str(self.id)

@app.route('/')
def home():
    return render_template('home.html', allpost=BlogPost.query.all())

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        temp = request.form
        data = BlogPost(title=temp['title'], content=temp['content'], author=temp['author'])
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

# The <> in url means the app take the thing in <> as an input,
# but you need to define the datatype and give it a name.
@app.route('/post/delete/<int:id_num>')
def delete(id_num):
    data = BlogPost.query.filter_by(id=id_num).first()
    db.session.delete(data)# if you want use filter_by() it needa go with .first()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/post/edit/<int:id_num>', methods=['GET', 'POST'])
def edit(id_num):
    # The PK col'id' start from 1
    data = BlogPost.query.filter_by(id=id_num).first()
    if request.method == 'POST':
        temp = request.form
        data.title = temp['title']
        data.content = temp['content']
        data.author = temp['author']
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('edit.html', num=id_num, allpost=data)

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)

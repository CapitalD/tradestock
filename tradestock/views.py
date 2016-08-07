from flask import render_template
from . import app, db
from models import Job, Stockitem

@app.route('/')
@app.route('/index')
def index():
    active_jobs = Job.query.filter_by(active=True).all()
    unallocated_stock = Stockitem.query.all()
    return render_template('index.html',
                    title='Tradestock - Home',
                    jobs=active_jobs,
                    stock=unallocated_stock)

from flask import render_template
from sqlalchemy import func
from . import app, db
from models import Job, Stockitem

@app.route('/')
@app.route('/index')
def index():

    active_jobs = db.session.query(Job, func.sum(Stockitem.quantity).label('stockcount'), func.sum(Stockitem.totalprice).label('stocksum')).outerjoin(Job.stockitems).group_by(Job).filter(Job.active==True).all()
    #active_jobs = Job.query.filter_by(active=True).all()
    unallocated_stock = Stockitem.query.filter(Stockitem.job==None).all()
    return render_template('index.html',
                    title='Tradestock - Home',
                    jobs=active_jobs,
                    unallocated_stock=unallocated_stock)

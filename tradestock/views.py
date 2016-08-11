from flask import render_template, flash, redirect, url_for
from sqlalchemy import func
from . import app, db
from models import Job, Stockitem
from forms import NewJobForm

@app.route('/')
@app.route('/index')
def index():

    active_jobs = db.session.query(Job, func.sum(Stockitem.quantity).label('stockcount'), func.sum(Stockitem.totalprice).label('stocksum')).outerjoin(Job.stockitems).group_by(Job).filter(Job.active==True).all()
    #active_jobs = Job.query.filter_by(active=True).all()
    unallocated_stock = Stockitem.query.filter(Stockitem.job==None).all()
    return render_template('index.html',
                    title='Home',
                    jobs=active_jobs,
                    unallocated_stock=unallocated_stock)

@app.route('/job/new', methods=['GET','POST'])
def new_job():
    form = NewJobForm()
    if form.validate_on_submit():
        job = Job(name=form.name.data, active=form.active.data)
        db.session.add(job)
        db.session.commit()
        flash('New job created: %s' %
            (form.name.data))
        return redirect(url_for('index'))
    return render_template('new_job.html',
                            title='Add job',
                            form=form)

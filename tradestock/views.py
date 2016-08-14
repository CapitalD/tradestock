from flask import render_template, flash, redirect, url_for
from sqlalchemy import func
from datetime import datetime
from . import app, db
from models import Job, Stockitem
from forms import NewJobForm, NewStockForm, AllocateStockForm, WriteoffStockForm

@app.route('/')
@app.route('/index')
def index():

    active_jobs = db.session.query(Job, func.sum(Stockitem.quantity).label('stockcount'), func.sum(Stockitem.totalprice).label('stocksum')).outerjoin(Job.stockitems).group_by(Job).filter(Job.active==True).all()
    #active_jobs = Job.query.filter_by(active=True).all()
    unallocated_stock = Stockitem.query.filter(Stockitem.job==None, Stockitem.writeoff==None).all()
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

@app.route('/stockitem/new', methods=['GET','POST'])
def new_stockitem():
    form = NewStockForm()
    jobs = [(j.id, j.name) for j in Job.query.filter_by(active=True).all()]
    form.job.choices = jobs
    form.job.choices.insert(0,(0,'Unallocated'))
    if form.validate_on_submit():
        totalprice = float(form.unitprice.data) * float(form.quantity.data)
        # TODO: Find a better alternative to using the value of 0 for the blank value, then handling two cases
        if form.job.data == 0:
            stockitem = Stockitem(sku=form.sku.data, name=form.name.data, unitprice=form.unitprice.data, quantity=form.quantity.data, totalprice=totalprice)
        else:
            stockitem = Stockitem(sku=form.sku.data, name=form.name.data, unitprice=form.unitprice.data, quantity=form.quantity.data, totalprice=totalprice, job_id=form.job.data)
        db.session.add(stockitem)
        db.session.commit()
        flash('New stockitem created: %s' %
            (form.name.data))
        return redirect(url_for('index'))
    return render_template('new_stockitem.html',
                            title='Add stockitem',
                            form=form)

@app.route('/stockitem/<id>/allocate', methods=['GET','POST'])
def allocate_stock(id):
    stockitem = Stockitem.query.get_or_404(id)
    form = AllocateStockForm(obj=stockitem)
    jobs = [(j.id, j.name) for j in Job.query.filter_by(active=True).all()]
    form.job.choices = jobs
    form.job.choices.insert(0,(0,'Unallocated'))
    # TODO: Find an alternative to updating the NumberRange validation via index.  It's yuck, but it works (at the moment).
    form.split_quantity.validators[0].max = stockitem.quantity
    if form.validate_on_submit():
        if form.split.data == "1": #all
            stockitem.job_id=form.job.data
        else:
            dupe_item = Stockitem(sku=stockitem.sku, name=stockitem.name, unitprice=stockitem.unitprice, quantity=stockitem.quantity)
            if form.split.data == "2": #quantity
                stockitem.quantity = float(form.split_quantity.data)
            if form.split.data == "3": #percentage
                stockitem.quantity = float(dupe_item.quantity) * (float(form.split_percentage.data) / 100)
            stockitem.totalprice = (float(stockitem.unitprice) * float(stockitem.quantity))
            stockitem.job_id=form.job.data
            dupe_item.quantity = (float(dupe_item.quantity) - float(stockitem.quantity))
            dupe_item.totalprice = (float(dupe_item.unitprice) * float(dupe_item.quantity))
            if dupe_item.quantity > 0:
                db.session.add(dupe_item)
        db.session.commit()
        flash('%s %s allocated to %s' %
            (stockitem.quantity, stockitem.name, stockitem.job.name))
        return redirect(url_for('index'))
    return render_template('allocate_stock.html',
                            title='Allocate stock to job',
                            form=form,
                            stockitem=stockitem)

@app.route('/stockitem/<id>/writeoff', methods=['GET','POST'])
def writeoff(id):
    stockitem = Stockitem.query.get_or_404(id)
    form = WriteoffStockForm(obj=stockitem)
    if form.validate_on_submit():
        stockitem.writeoff = datetime.utcnow()
        db.session.commit()
        flash('%s written off' % (stockitem.name))
        return redirect(url_for('index'))
    return render_template('writeoff_stock.html',
                            title='Write-off stock',
                            form=form,
                            stockitem=stockitem)

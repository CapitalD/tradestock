from flask import render_template, flash, redirect, url_for
from sqlalchemy import func
from . import app, db
from models import Job, Stockitem
from forms import NewJobForm, NewStockForm, AllocateStockForm

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
        if form.split.data == "2":
            dupe_item = Stockitem(sku=stockitem.sku, name=stockitem.name, unitprice=stockitem.unitprice, quantity=stockitem.quantity)
            stockitem.quantity = float(form.split_quantity.data)
            stockitem.totalprice = (float(stockitem.unitprice) * float(stockitem.quantity))
            stockitem.job_id=form.job.data
            dupe_item.quantity = (float(dupe_item.quantity) - float(form.split_quantity.data))
            dupe_item.totalprice = (float(dupe_item.unitprice) * float(dupe_item.quantity))
            db.session.add(dupe_item)
            db.session.commit()
        elif form.split.data == "3":
            print "split 3 %"
            # duplicate stockitem
            # update quanity of one to form.split_percentage, and allocate to selected job
            # update the quantity of the other to (stockitem.quantity - form.split_quantity)
            # save both
        else:
            print "split 1 (all)"
        db.session.commit()
        flash('Stockitem allocated to job: %s' %
            (stockitem.job.name))
        return redirect(url_for('index'))
    return render_template('allocate_stock.html',
                            title='Allocate stock to job',
                            form=form,
                            stockitem=stockitem)

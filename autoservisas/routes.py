from datetime import datetime
from flask import redirect, request, render_template, flash, url_for, abort
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_user, login_required, current_user
from autoservisas.models import Vartotojas, Car, Gedimas, AdminModel
from autoservisas import forms
from autoservisas import app, db, admin

admin.add_view(AdminModel(Vartotojas, db.session))
admin.add_view(AdminModel(Car, db.session))
admin.add_view(AdminModel(Gedimas, db.session))
bcrypt = Bcrypt(app)

@app.route('/admin')
@login_required
def admin():
    return redirect(url_for(admin))

@app.route('/')
def home():
    flash('Sveiki atvykę!', 'info')
    return render_template('base.html', current_user=current_user) 

@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if current_user.is_authenticated:
        flash('Atsijunkite, kad priregistruoti naują vartotoją.')
        return redirect(url_for('home'))
    form = forms.RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        naujas_vartotojas = Vartotojas(
            vardas = form.vardas.data,
            el_pastas = form.el_pastas.data,
            slaptazodis = koduotas_slaptazodis
        )
        db.session.add(naujas_vartotojas)
        db.session.commit()
        
        flash('Sėkmingai prisiregistravote!', 'success')
        return redirect(url_for('home'))
    return render_template('registracija.html', form=form, current_user=current_user)


@app.route('/prisijungimas', methods=['GET', 'POST'])
def prisijungimas():
    next_page = request.args.get('next')
    if current_user.is_authenticated:
        flash('Vartotojas jau prisijungęs. Atsijunkite ir bandykite iš naujo.', 'danger')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            # First user is always admin
            if current_user == Vartotojas.query.first():
                current_user.is_admin = True
                db.session.commit()
            if current_user.is_admin:
                flash('Jūs esate administratorius.', 'warning')
            elif current_user.is_employee:
                flash('Jūs esate darbuotojas.', 'warning')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Prisijungti nepavyko, neteisingas el.paštas arba slaptažodis.', 'danger')
    return render_template('prisijungimas.html', form=form, current_user=current_user)

@app.route('/atsijungimas')
def atsijungimas():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))


@app.route('/profilis', methods=['GET', 'POST'])
@login_required
def profilis():
    form = forms.ProfilioForma()
    if form.validate_on_submit():
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash('Profilis atnaujintas!', 'success')
        return redirect(url_for('profilis'))
    elif request.method == "GET":
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
    return render_template('profilis.html', current_user=current_user, form=form)

@app.route('/uzsirasyti', methods=['GET', 'POST'])
@login_required
def uzsirasyti():
    if current_user.is_admin or current_user.is_employee:
        abort(403)
    else:
        form = forms.CarForma()
        if form.validate_on_submit():
            vartotojas = current_user.id
            naujas_irasas = Car(
                modelis = form.modelis.data,
                marke = form.marke.data,
                gaminimo_metai = form.gaminimo_metai.data,
                variklis = form.variklis.data,
                valst_numeris = form.valst_numeris.data,
                vin = form.vin.data,
                vartotojas_id = vartotojas
            )
            db.session.add(naujas_irasas)
            db.session.commit()
            flash('Mašina užregistruota.', 'success')
            return redirect(url_for('uzsirasyti'))
    return render_template('uzsirasyti.html', form=form, current_user=current_user)

@app.route('/gedimas', methods=['GET', 'POST'])
@login_required
def gedimas():
    if current_user.is_admin or current_user.is_employee:
        abort(403)
    else:
        form = forms.GedimoForma()
        if form.validate_on_submit():
            naujas_irasas = Gedimas(
                gedimas = form.gedimas.data, 
                masina_id = form.masina.data.id  
            )
            db.session.add(naujas_irasas)
            db.session.commit()
            form.gedimas.data = ''
            flash('Gedimas užregistruotas', 'success')
    return render_template('gedimas.html', form=form)


@app.route('/irasai')
@login_required
def records():
    page = request.args.get('page', 1, type=int)
    if current_user.is_employee:
        visi_irasai = Car.query.filter_by().order_by(Car.sukurta.desc()).paginate(page=page, per_page=5)
    else:
        visi_irasai = Car.query.filter_by(vartotojas_id=current_user.id).order_by(Car.sukurta.desc()).paginate(page=page, per_page=5)
    return render_template('irasai.html', visi_irasai=visi_irasai, datetime=datetime)

@app.route('/irasai/<int:masina_id>/delete', methods=['GET', 'POST'])
@login_required
def pasalinti_masina(masina_id):
    if current_user.is_admin:
        abort(403)
    else:
        masina = Car.query.filter_by(id=masina_id).first()
        db.session.delete(masina)
        db.session.commit()
        flash('Mašina pašalinta.', 'success')
    return render_template('irasai.html', masina_id=masina_id)

@app.route('/gedimu_istorija/<int:masina_id>')
@login_required
def gedimu_istorija(masina_id):
    busena = [{'name': 'Remontuojama'}, {'name': 'Suremontuota'}, {'name': 'Laukiama detalių'}]
    visi_gedimai = Gedimas.query.filter_by(masina_id=masina_id).all()
    return render_template('gedimu_istorija.html', visi_gedimai=visi_gedimai, busena=busena, datetime=datetime)

@app.route('/gedimu_istorija/<int:gedimas_id>', methods=['GET', 'POST'])
@login_required
def keisti_busena(gedimas_id):
    busena = request.form.get('busena')
    kaina = request.form.get('price')
    gedimas = Gedimas.query.filter_by(id=gedimas_id).first()
    gedimas.gedimo_busena = busena
    gedimas.gedimo_kaina = kaina
    db.session.commit()
    flash('Būsena atnaujinta', 'success')
    return render_template('gedimu_istorija.html', gedimas_id=gedimas_id)

@app.route('/gedimu_istorija/<int:gedimas_id>/delete', methods=['GET','POST'])
@login_required
def pasalinti_gedima(gedimas_id):
    if not current_user.is_employee:
        abort(403)
    else:
        gedimas = Gedimas.query.filter_by(id=gedimas_id).first()
        db.session.delete(gedimas)
        db.session.commit()
        flash('Gedimo įrašas pašalintas.', 'success')
    return render_template('gedimu_istorija.html', gedimas=gedimas, gedimas_id=gedimas_id)



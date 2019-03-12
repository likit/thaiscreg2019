from flask import render_template, redirect, request, url_for
from . import mainbp as main
from .forms import SignUpForm, LogInForm
from collections import defaultdict
from .models import User
from ..app import db
from flask_login import login_user, current_user, logout_user

@main.route('/', methods=['GET', 'POST'])
def index():
    error_msg = defaultdict(list)
    form = SignUpForm()
    if form.validate_on_submit():
        user_ = User.query.filter_by(email=form.email.data).first()
        if user_:
            return redirect('/')
        else:
            new_user = User(email=form.email.data,
                            password=form.password1.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return '{} has been logged in.'.format(current_user.email)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                error_msg[field].append(error)

    return render_template('main/index.html', form=form, error_msg=error_msg)


@main.route('/login_form', methods=['GET', 'POST'])
def log_user_in():
    error_msg = None
    form = LogInForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            pw = request.form.get('password')
            if pw == user.password:
                login_user(user)
                return redirect('/')
            else:
                error_msg = 'Password is not correct.'
        else:
            error_msg = 'Email does not exist.'

    return render_template('main/login.html', form=form,
                           error_msg=error_msg)


@main.route('/logout_form', methods=['GET', 'POST'])
def log_user_out():
    if current_user.is_authenticated:
        form = LogInForm()
        logout_user()
        return render_template('main/logout.html', form=form)
    else:
        return redirect(url_for('main.log_user_in'))

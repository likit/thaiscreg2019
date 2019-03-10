from flask import render_template, redirect, request
from . import mainbp as main
from .forms import LoginForm
from collections import defaultdict
from .models import User
from ..app import db
from flask_login import login_user, current_user

@main.route('/', methods=['GET', 'POST'])
def index():
    error_msg = defaultdict(list)
    form = LoginForm()
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


from flask import render_template, redirect, request
from . import mainbp as main
from .forms import LoginForm
from collections import defaultdict

@main.route('/', methods=['GET', 'POST'])
def index():
    error_msg = defaultdict(list)
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                error_msg[field].append(error)

    return render_template('main/index.html', form=form, error_msg=error_msg)


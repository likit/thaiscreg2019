from flask import render_template, redirect, request, url_for
from . import mainbp as main
from .forms import SignUpForm, LogInForm
from collections import defaultdict
from .models import User, Project, Event
from ..app import db
from flask_login import login_user, current_user, logout_user, login_required

@main.route('/', methods=['GET', 'POST'])
def index():
    error_msg = defaultdict(list)
    form = SignUpForm()
    if form.validate_on_submit():
        user_ = User.query.filter_by(email=form.email.data).first()
        if user_:
            return redirect(url_for('main.log_user_in', user_exist=form.email.data))
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

    projects = Project.query.all()[:3]
    events = Event.query.all()[:5]

    return render_template('main/index.html', form=form,
                           error_msg=error_msg,
                           projects=projects,
                           events=events,
                           )


@main.route('/login_form', methods=['GET', 'POST'])
def log_user_in():
    error_msg = None
    if current_user.is_authenticated:
        return redirect(url_for('main.account_dash'))
    form = LogInForm()
    if request.args.get('user_exist', False):
        error_msg = 'Email account already exists. Please log in.'
        form.email.data = request.args.get('user_exist')
    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            pw = request.form.get('password')
            if pw == user.password:
                login_user(user, remember=True)
                return redirect('/')
            else:
                error_msg = 'Password is not correct.'
        else:
            error_msg = 'Email does not exist.'

    return render_template('main/login.html', form=form,
                           error_msg=error_msg)


@main.route('/logout_form', methods=['GET', 'POST'])
@login_required
def log_user_out():
    if current_user.is_authenticated:
        form = LogInForm()
        logout_user()
        return render_template('main/logout.html', form=form)
    else:
        return redirect(url_for('main.log_user_in'))


@main.route('/account/dashboard')
@login_required
def account_dash():
    projects = {'pending': 0, 'approved': 0, 'total': 0}
    affil_researchers = []
    affil_projects = {'pending': 0, 'approved': 0, 'total': 0}
    for researcher in current_user.profile.affil.affiliates:
        for proj in researcher.user.created_projects:
            if proj.status.status == 'pending':
                affil_projects['pending'] += 1
            elif proj.status.status == 'approved':
                affil_projects['approved'] += 1
        affil_projects['total'] += 1
        affil_researchers.append(researcher)

    for proj in current_user.created_projects:
        if proj.status.status == 'pending':
            projects['pending'] += 1
        elif proj.status.status == 'approved':
            projects['approved'] += 1
        projects['total'] += 1
    return render_template('main/account_dash.html',
                           projects=projects,
                           affil_projects=affil_projects,
                           affil_researchers=affil_researchers,
                           page_name='dashboard')


@main.route('/account/projects')
@login_required
def account_projects():
    status_filter = request.args.get('status_filter', None)
    projects = []
    for proj in current_user.created_projects:
        projects.append({
            'id': proj.id,
            'title': proj.title,
            'affil': proj.institution.name_th,
            'startdate': proj.startdate,
            'enddate': proj.enddate,
            'status': proj.status.status,
            'creator': {
                'email': proj.creator.email,
                'firstname': proj.creator.profile.first_name_th,
                'lastname': proj.creator.profile.last_name_th,
                'affil': proj.creator.profile.affil.name_th,
            },
            'summary': proj.summary[:300]
        })

    if status_filter is None or status_filter == 'all':
        filtered_projects = projects
        status_filter = None
    else:
        filtered_projects = [p for p in projects if p['status'] == status_filter]

    return render_template('main/account_projects.html',
                           projects=filtered_projects,
                           status_filter=status_filter,
                           page_name='project')


@main.route('/projects')
def show_projects():
    query = request.args.get('q', None)
    projects = []
    for proj in Project.query.all():
        projects.append({
            'id': proj.id,
            'title': proj.title,
            'affil': proj.institution.name_th,
            'startdate': proj.startdate,
            'enddate': proj.enddate,
            'status': proj.status.status,
            'creator': {
                'email': proj.creator.email,
                'firstname': proj.creator.profile.first_name_th,
                'lastname': proj.creator.profile.last_name_th,
                'affil': proj.creator.profile.affil.name_th,
            },
            'summary': proj.summary[:300]
        })

    if query:
        filtered_projects = []
        for p in projects:
            if query.lower() in p['title'].lower() or query.lower() in p['summary'].lower():
                filtered_projects.append(p)
    else:
        filtered_projects = projects
    return render_template('main/projects.html',
                           query=query,
                           projects=filtered_projects)


from datetime import datetime
from flask import render_template, redirect, request, url_for
from . import mainbp as main
from .forms import SignUpForm, LogInForm, ProfileForm, RegisterCellForm, RegisterProjectForm
from collections import defaultdict
from .models import User, Project, Event, Cell, ApprovalStatus, Institution
from .models import InstitutionSchema
from ..app import db
from flask_login import login_user, current_user, logout_user, login_required
from json import loads


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
    cells = Cell.query.all()[:5]

    return render_template('main/index.html', form=form,
                           error_msg=error_msg,
                           projects=projects,
                           events=events,
                           cells=cells,
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


@main.route('/project/<int:project_id>')
def display_project_info(project_id):
    project = Project.query.get(project_id)
    return render_template('main/project_detail.html', project=project)


@main.route('/account/profile/edit', methods=['POST', 'GET'])
@login_required
def edit_profile():
    msg = None
    error_msg = {}
    pf = current_user.profile
    form = ProfileForm()
    if form.validate_on_submit():
        pf.public_email = form.public_email.data
        pf.academic_title_th = form.academic_title_th.data
        pf.title_th = form.title_th.data
        pf.first_name_en = form.firstname_en.data
        pf.last_name_en = form.lastname_en.data
        pf.first_name_th = form.firstname_th.data
        pf.last_name_th = form.lastname_th.data
        pf.phone = form.phone.data
        pf.street = form.street.data
        db.session.add(pf)
        db.session.commit()
        msg = 'Your profile has been updated.'
    else:
        for field, errors in form.errors.items():
            for error in errors:
                error_msg[field].append(error)

    form.public_email.data = pf.public_email
    form.title_th.data = pf.title_th
    form.academic_title_th.data = pf.academic_title_th
    form.firstname_th.data = pf.first_name_th
    form.lastname_th.data = pf.last_name_th
    form.firstname_en.data = pf.first_name_en
    form.lastname_en.data = pf.last_name_en
    form.street.data = pf.street
    form.phone.data = pf.phone

    return render_template('main/edit_profile.html', form=form,
                           message=msg, error_msg=error_msg,
                           page_name='profile')


@main.route('/account/cells', methods=['GET', 'POST'])
@login_required
def account_cells():
    cells = []
    for c in current_user.own_cells:
        cells.append({
            'id': c.id,
            'institution_id': c.institution.id,
            'institution_name': c.institution.name_th,
            'institution_campus': c.institution.campus,
            'cell_type': c.cell_type,
            'alt_names': c.data.get('alt_names', ''),
            'submitted_by': u'{} {} ({} {})'.format(
                c.user.profile.first_name_th,
                c.user.profile.last_name_th,
                c.user.profile.first_name_en,
                c.user.profile.last_name_en),
            'submitter_email': c.user.email,
            'status': c.status.status,
            'register_datetime': c.register_datetime,
            'update_datetime': c.update_datetime,
            'last_view': c.last_view,
            'data': c.data,
            'view_count': c.view_count or 0,
        })
    return render_template('main/account_cells.html',
                           page_name='cell',
                           cells=cells)


@main.route('/cell/register', methods=['GET', 'POST'])
@login_required
def register_cell():
    form = RegisterCellForm()
    institutions = [(str(current_user.profile.affil.id),
                     current_user.profile.affil.name_th)]
    form.institution.choices = institutions
    form.institution.default = institutions[0][0]
    pending_status = ApprovalStatus.query.filter_by(status='pending').first()

    if form.validate_on_submit():
        markers = request.form.get('markerData', '')
        markers = loads(markers)
        print('form validated!')
        print(form.institution.data, form.comment.data, form.cell_type.data, form.available.data)
        data = {
            'alt_names': form.alternative_names.data,
            'comment': form.comment.data,
            'availability': form.available.data,
            'donor': {
                'sex': form.donor_gender.data,
                'karyotyped': form.donor_karyotyped.data,
                'diseases': form.donor_diseases.data,
                'disease_associated_phenotypes': form.donor_disease_assoc_phenotypes.data,
                'genome_wide_study': form.donor_gws.data,
            },
            'culture': {
                'surface_coating': form.culture_surface_coating.data,
                'feeder_cells': form.culture_feeder_cells.data,
                'co2_conc': str(form.culture_co2_conc.data) if form.culture_co2_conc else '',
                'o2_conc': str(form.culture_o2_conc.data) if form.culture_o2_conc else '',
                'medium': form.culture_medium.data,
                'passage_method': form.culture_passage_method.data,
                'rock_inhibitor_cryo': form.culture_rock_inhibitor_used_at_cryo.data,
                'rock_inhibitor_passage': form.culture_rock_inhibitor_used_at_passage.data,
                'rock_inhibitor_thaw': form.culture_rock_inhibitor_used_at_thaw.data,
            },
            'characterization': {
                'markers': markers,
                'endoderm_potency': form.diff_potency_endoderm.data,
                'ectoderm_potency': form.diff_potency_ectoderm.data,
                'mesoderm_potency': form.diff_potency_mesoderm.data,
            },
            'genotyping': {
                'karyotyped': form.karyotyped.data,
                'karyotype': form.karyotype.data,

            },
            'msc': {
                'source_cell_origin': form.source_cell_origin.data,
            },
            'hipsc': {
                'source_cell_origin': form.source_cell_origin.data,
                'source_cell_type': form.source_cell_type.data,
                'age_of_collection': form.donor_age_collection.data,
                'collected_in': form.collected_in.data,
                'vector_type': form.vector_type.data,
                'vector': form.vector.data,
                'selection_criteria': form.selection_criteria.data,
                'derived_condition': {
                    'xeno_free': form.xeno_free.data,
                    'under_gmp': form.under_gmp.data,
                },
                'clinical_grade_available': form.clinical_grade_avail.data
            },
            'hesc': {
                'embryo_stage': form.embryo_stage.data,
                'ivf_treatment': form.ivf_treatment.data,
                'pgd_embryo': form.pgd_embryo.data,
                'zp_removal_technique': form.zp_removal_technique.data,
                'cell_isolation': form.cell_isolation.data,
                'cell_seeding': form.cell_seeding.data,
            },
        }
        print(data)
        cell = Cell(
            institution_id=int(form.institution.data),
            cell_type=form.cell_type.data,
            user=current_user,
            data=data,
            status=pending_status,
            register_datetime=datetime.utcnow(),
            update_datetime=datetime.utcnow(),
        )
        db.session.add(cell)
        db.session.commit()
        return redirect(url_for('main.account_cells'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(field, error)

    return render_template('main/register_cell.html', form=form)


@main.route('/cell/<int:cell_id>', methods=['GET', 'POST'])
def display_cell_info(cell_id=None):
    if cell_id:
        cell = Cell.query.get(cell_id)
        cell.view_count += 1
        cell.last_view = datetime.utcnow()
        db.session.add(cell)
        db.session.commit()
        return render_template('main/cell_detail.html', cell=cell)


@main.route('/project/register', methods=['GET', 'POST'])
@login_required
def register_project():
    institution_schema = InstitutionSchema(many=True)
    form = RegisterProjectForm()
    institutions = Institution.query.all()
    if form.validate_on_submit():
        print(request.form.get('hidden_startdate'), request.form.get('hidden_enddate'))
    else:
        print(request.form.get('hidden_institution'))
    return render_template('main/register_project.html',
                            form=form,
                            institutions=institution_schema.dump(institutions).data)


@main.route('/cells', methods=['GET', 'POST'])
def show_cell_list():
    cell_type = request.args.get('cell-type', 'all')
    cells = []
    for c in Cell.query.all():
        cells.append({
            'id': c.id,
            'institution_id': c.institution.id,
            'institution_name': c.institution.name_th,
            'institution_campus': c.institution.campus,
            'cell_type': c.cell_type,
            'alt_names': c.data.get('alt_names', ''),
            'submitted_by': u'{} {} ({} {})'.format(
                c.user.profile.first_name_th,
                c.user.profile.last_name_th,
                c.user.profile.first_name_en,
                c.user.profile.last_name_en),
            'submitter_email': c.user.email,
            'status': c.status.status,
            'register_datetime': c.register_datetime,
            'update_datetime': c.update_datetime,
            'last_view': c.last_view,
            'data': c.data,
            'view_count': c.view_count or 0,
        })
        if cell_type != 'all':
            filtered_cells = [c for c in cells if c['cell_type'] == cell_type]
        else:
            filtered_cells = cells
    return render_template('main/cells.html',
                           page_name='cell',
                           cells=filtered_cells)

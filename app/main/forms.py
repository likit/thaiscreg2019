from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, DecimalField, HiddenField,
                     RadioField, SelectField, BooleanField, DateField, IntegerField)
from wtforms.widgets import TextArea
from wtforms.validators import Email, DataRequired, Length, EqualTo, optional


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password',
                              validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(),
                                          EqualTo('password1',
                                                  message="Passwords do not match.")])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Submit')


class ProfileForm(FlaskForm):
    public_email = StringField('Public Email', validators=[Email()])
    title_th = StringField('Title', validators=[Length(max=128)])
    academic_title_th = StringField('Academic Title', validators=[Length(max=128)])
    firstname_en = StringField('English First Name')
    lastname_en = StringField('English Last Name')
    firstname_th = StringField('Thai First Name')
    lastname_th = StringField('Thai Last Name')
    phone = StringField('Phone')
    street = StringField('Street', widget=TextArea())
    submit = SubmitField('Submit')


class RegisterCellForm(FlaskForm):
    cell_type = RadioField('Cell Type',
                           choices=[('hiPSC', 'hiPSC'), ('hESC', 'hESC'), ('MSC', 'MSC')],
                           default='hiPSC',
                           validators=[DataRequired()])
    institution = SelectField('Institution',
                              validators=[DataRequired(), ])
    comment = StringField('Comment', widget=TextArea())
    alternative_names = StringField('Alternative Name(s)')
    available = SelectField('Availability', choices=[
        ('0', 'Available with no restrictions'),
        ('1', 'Available for Non-commercial Research')
    ])
    karyotyped = SelectField('Has the cell line been karyotyped?',
                             choices=[('no', 'No'), ('yes', 'Yes')],
                             default='no')
    karyotype = StringField('Karyotype')
    source_cell_type = StringField('Source cell type')
    source_cell_origin = StringField('Source cell origin')
    donor_age_collection = IntegerField('Age of donor (at collection)', validators=[optional()])
    collected_in = IntegerField('Collected in', validators=[optional()])
    passage_no = IntegerField('Passage number reprogrammed')
    vector_type = SelectField('Vector type', choices=[('Non-integrating', 'Non-integrating')],
                              validators=[optional()])
    vector = StringField('Vector')
    selection_criteria = StringField('Selection criteria for clones')
    xeno_free = SelectField('Derived under xeno-free conditions',
                            choices=[('no', 'No'), ('yes', 'Yes')],
                            default='no')
    under_gmp = SelectField('Derived under GMP?',
                            choices=[('no', 'No'), ('yes', 'Yes')],
                            default='no')
    clinical_grade_avail = SelectField('Available as clinical grade?',
                                       choices=[('no', 'No'), ('yes', 'Yes')],
                                       default='no')
    donor_gender = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female')],
                               default='male')
    donor_diseases = StringField('Diseases')
    donor_disease_assoc_phenotypes = StringField('Disease associated phenotypes')
    donor_karyotyped = SelectField('Has the donor karyotype been analyzed?',
                                   choices=[('no', 'No'), ('yes', 'Yes')],
                                   default='no')
    donor_gws = SelectField('Is there genome-wide genotyping or functional data available?',
                            choices=[('no', 'No'), ('yes', 'Yes')],
                            default='no')
    culture_surface_coating = StringField('Surface Coating')
    culture_feeder_cells = SelectField('Feeder cells',
                                       choices=[('no', 'No'), ('yes', 'Yes')],
                                       validators=[optional()])
    culture_passage_method = StringField('Passage Method')
    culture_o2_conc = DecimalField('O2 Concentration', validators=[optional()])
    culture_co2_conc = DecimalField('CO2 Concentration', validators=[optional()])
    culture_medium = StringField('Medium')
    culture_rock_inhibitor_used_at_passage = SelectField('Has Rock inhibitor (Y27632) been used at passage previously with this cell line?',
                                                         choices=[('no', 'No'), ('yes', 'Yes')],
                                                         default='no')
    culture_rock_inhibitor_used_at_cryo = SelectField('Has Rock inhibitor (Y27632) been used at cryo previously with this cell line?',
                                                      choices=[('no', 'No'), ('yes', 'Yes')],
                                                      default='no')
    culture_rock_inhibitor_used_at_thaw = SelectField('Has Rock inhibitor (Y27632) been used at thaw previously with this cell line?',
                                                      choices=[('no', 'No'), ('yes', 'Yes')],
                                                      default='no')
    character = HiddenField('Characteristics')
    diff_potency_endoderm = StringField('Endoderm')
    diff_potency_mesoderm = StringField('Mesoderm')
    diff_potency_ectoderm = StringField('Ectoderm')

    embryo_stage = StringField('Embryo Stage')
    ivf_treatment = SelectField('Supernumerary embryos from IVF treatment?',
                                choices=[('no', 'No'), ('yes', 'Yes')],
                                default='no')
    pgd_embryo = SelectField('PGD Embryo?',
                             choices=[('no', 'No'), ('yes', 'Yes')],
                             default='no')
    zp_removal_technique = StringField('ZP removal technique')
    cell_isolation = StringField('Cell isolation')
    cell_seeding = StringField('Cell seeding')


    marker_Alkaline_Phosphatase_enzyme = StringField('Enzymatic Assay')
    marker_Alkaline_Phosphatase_expr_profile = StringField('Expression Profiles')

    submit = SubmitField('Submit')


class RegisterProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    acronym = StringField('acronym')
    summary = StringField('summary', widget=TextArea())
    website = StringField('website')
    startdate = DateField('Start Date', validators=[optional()])
    enddate = DateField('End Date', validators=[optional()])
    sponsor_name = StringField('Sponsor Name')
    institution = StringField('Institution Name')
    submit = SubmitField('Submit')

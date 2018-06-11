import os
import re
from flask import (
    Flask, request,
    session, redirect,
    url_for, render_template,
    flash)
import forms as fs
from werkzeug import secure_filename
import tempfile
import copath_nls
import meditech_nls


ALLOWED_EXTENSIONS = set(['txt'])
fapp = Flask(__name__)
fapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
fapp.debug = True


@fapp.route('/index',  methods=['GET', 'POST'])
@fapp.route('/',  methods=['GET', 'POST'])
def index():
    form = fs.InputForm()
    form_file = fs.FileInputForm()
    for f in os.listdir(os.path.join(os.getcwd(), 'temp', 'lock')):
        os.remove(os.path.join(os.getcwd(), 'temp', 'lock', f))
    if request.method == 'GET':
        return render_template('index.html', form=form, form_file=form_file)
    if request.method == 'POST':
        if request.form['choice_site'] == 'UM':
            form.choice_spec.choices = [('', ''), ('US', 'US'),
                                        ('UB', 'UB'), ('UT', 'UT'),
                                        ('M', 'M'), ('UC', 'UC'), ('C', 'C')]
        if request.form['choice_site'] == 'JHS':
            form.choice_spec.choices = [('', ''), ('S', 'S'),
                                        ('US', 'US'), ('T', 'T'),
                                        ('C', 'C'), ('H', 'H'),
                                        ('SB', 'SB'), ('M', 'M'),
                                        ('F', 'F'), ('A', 'A'),
                                        ('SS', 'SS'), ('NS', 'NS')]
        if request.form['choice_site'] == 'NY':
            form.choice_spec.choices = [('', ''), ('S', 'S'),
                                        ('C', 'C')]
        if request.form['choice_site'] == 'meditech':
            form.choice_spec.choices = [('', ''), ('C', 'C'), ('UM', 'UM'),
                                        ('A', 'A')]

        if (form.validate_on_submit() is False) or (form_file.validate_on_submit() is False):
            flash('Input is incomplete!')
            return render_template('index.html', form=form, form_file=form_file)

        if form.validate_on_submit() and form_file.validate_on_submit():
            filename = secure_filename(form_file.openfile.data.filename)
            form_file.openfile.data.save(os.path.join(os.getcwd(), 'temp', filename))
            params = dict(request.form)
            params.pop('csrf_token')
            out_dir = re.sub('[^\w]', '_', params['out_dir'][0], re.S)
            params['out_dir'] = os.path.join(os.getcwd(), 'job_output', out_dir)
            params['openfile'] = os.path.join(os.getcwd(), 'temp', filename)
            params['choice_site'] = params['choice_site'][0]
            session['params'] = params
            return redirect(url_for('wait', site=request.form['choice_site']))


@fapp.route('/wait',  methods=['GET', 'POST'])
def wait():

    if request.method == 'GET':
        os.makedirs(session['params']['out_dir'])
        with tempfile.NamedTemporaryFile('wt', dir=os.path.join(os.getcwd(), 'temp', 'lock'), delete=False) as tf:
            temp_str = 'parsing copath NLS job'
            tf.write(temp_str)
            tempname = tf.name

        if request.args['site'] in ['UM', 'JHS', 'NY']:
            case_counts, parsed_cases_counts, excel_truncation = copath_nls.copath_parse(session['params'])
        elif request.args['site'] in ['meditech']:
            case_counts, parsed_cases_counts, excel_truncation = meditech_nls.meditech_parse(session['params'])

        os.remove(tempname)
        os.remove(os.path.join(os.getcwd(), 'temp', session['params']['openfile']))

        return render_template(
            'wait.html',
            case_counts=case_counts,
            parsed_cases_counts=parsed_cases_counts,
            excel_truncation=excel_truncation)

    if request.method == 'POST':
        while len(os.listdir(os.path.join(os.getcwd(), 'temp', 'lock'))) > 0:
            pass
        return redirect(url_for('index'))


@fapp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


fapp.run()

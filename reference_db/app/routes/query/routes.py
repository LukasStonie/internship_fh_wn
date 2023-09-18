from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required

from app.forms.forms import QueryForm
from app.models.model import Peak, Spectrum, Compound, Intensity
from app.routes.query import bp
from app.extensions import db


@bp.route('/query', methods=['GET'])
@login_required
def query():
    form = QueryForm()
    return render_template('resources/query/index.html', form=form)


def get_form_data(form):
    # get evey key-value pair from the form where the key contains '_intensity'
    data = {float(k.lstrip("wn-")): float(v) for k, v in form.items() if 'wn-' in k and v != ''}
    return data, float(form['tolerance'])


@bp.route('/query', methods=['POST'])
@login_required
def query_post():
    data, tolerance = get_form_data(request.form)
    if  len(data) == 0:
        flash('Bitte geben Sie mindestens eine Wellenzahl an.', 'danger')
        return redirect(url_for('query.query'))
    # query peaks table for peaks with wavenumber in data and in given tolerance
    wavenumbers = {}
    cnt = 0
    for wavenumber in data.values():
        peaks = db.session.query(Peak).filter(
            Peak.wavenumber.between(wavenumber - tolerance, wavenumber + tolerance)).all()
        result = []
        for peak in peaks:
            result_element = {}
            spectrum = db.session.query(Spectrum).filter(Spectrum.id == peak.spectrum_id).first()
            compound = db.session.query(Compound).filter(Compound.id == spectrum.compound_id).first()
            result_element['compound'] = compound.name
            result_element['compound_id'] = compound.id
            result_element['exact_wavenumber'] = peak.wavenumber
            result_element['intensity'] = db.session.query(Intensity).filter(
                Intensity.id == peak.intensity_id).first().shorthand
            result.append(result_element)
            cnt += 1
        wavenumbers[wavenumber] = result
    return render_template('resources/query/result.html', result=dict(sorted(wavenumbers.items())), tolerance=tolerance, cnt=cnt)

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models.user_settings import UserSettings
from .forms import ProfileForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    settings = current_user.settings  # current user-oda settings mattum
    form = ProfileForm(obj=settings)
    if form.validate_on_submit():
        if settings is None:
            settings = UserSettings(user_id=current_user.id)
            db.session.add(settings)
        settings.full_name = (form.full_name.data or '').strip() or None
        settings.age = form.age.data
        settings.family_members = form.family_members.data
        settings.risk_tolerance = form.risk_tolerance.data
        settings.horizon_years = form.horizon_years.data
        settings.emergency_target_months = form.emergency_target_months.data
        db.session.commit()
        flash('Profile saved.', 'success')
        return redirect(url_for('profile.index'))
    return render_template('profile/index.html', form=form)
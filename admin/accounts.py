"""Admin Accounts"""
from flask import abort, Blueprint, flash, render_template
from flask_login import current_user

from database import db_session
from forms import EditAccountForm
from models import Account
from sentry import sentry_sdk


# Flask Blueprints
from admin.players import players
accounts = Blueprint(
    'accounts',
    __name__,
    url_prefix='/accounts',
    template_folder='templates/accounts'
)
accounts.register_blueprint(players)


@accounts.route('/', methods=['GET'])
def index():
    """Administration portal to allow Gods to view accounts
        /admin/accounts"""
    return render_template(
        'accounts.html.j2',
        accounts=Account.query.order_by(Account.account_id).all()
    )


@accounts.route('/manage/<int:manage_account_id>/', methods=['GET'])
@accounts.route('/manage/<int:manage_account_id>', methods=['GET'])
def manage(manage_account_id=None):
    """Administration portal to allow Gods to view accounts
        /admin/account"""
    account = Account.query.filter_by(account_id=manage_account_id).first()

    # 400 if bad account
    if not account:
        flash('Invalid account.', 'error')
        abort(400)

    return render_template(
        'manage_account.html.j2',
        manage_account=account
    )


@accounts.route('/edit/<int:edit_account_id>/', methods=['GET', 'POST'])
@accounts.route('/edit/<int:edit_account_id>', methods=['GET', 'POST'])
def edit(edit_account_id=None):
    """Administration portal to allow Gods to edit accounts
        /admin/accounts/edit"""
    account = Account.query.filter_by(account_id=edit_account_id).first()

    # 400 if bad account
    if not account:
        flash('Invalid account.', 'error')
        abort(400)

    # Get edit account form and check if submitted
    edit_account_form = EditAccountForm()
    if edit_account_form.validate_on_submit():

        # Update database with submitted form values
        account.account_name = edit_account_form.account_name.data
        account.email = edit_account_form.email.data
        account.seasonal_points = edit_account_form.seasonal_points.data

        # Process administrative password reset
        if edit_account_form.confirm_password.data:
            if account.change_password(
                new_password=edit_account_form.confirm_password.data
            ):
                flash(
                    f'The account ({account.name}) password was reset.',
                    'success'
                )
                sentry_sdk.capture_message(
                    f'Admin Password Reset: {current_user} reset {account}'
                )
        db_session.commit()
        flash('The account was updated successfully.', 'success')
        sentry_sdk.capture_message(
            f'Admin Edit Account: {current_user} edited {account}'
        )

    return render_template(
        'edit_account.html.j2',
        edit_account=account,
        edit_account_form=edit_account_form
    )

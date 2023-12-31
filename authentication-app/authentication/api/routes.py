from flask import Blueprint, render_template


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/members')
def list_member(id=None):

    return render_template('page.html', name=name)
from flask import Blueprint, make_response, request, jsonify


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/', methods=['GET'])
def api_root(id=None):
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    response = {'response': 'It Works!'}
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(response), 200, headers)

@api.route('/member/<string:student_id>')
def member_profile(student_id=None):
    pass
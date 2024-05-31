from flask import Blueprint, make_response, request, jsonify
from authentication.controller.MemberController import MemberController
#from authentication.


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/', methods=['GET'])
def api_root(id=None):
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    response = {'response': 'It Works!'}
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(response), 200, headers)


@api.route('/member/<string:chip_id>', methods=['POST'])
def check_auth_member(chip_id=None):
    if request.method != 'POST':
        return make_response('Malformed request', 400)
    
    response = {'response': 'It Works!'}
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(response), 200, headers)

# ================= RESTful APIs Member =================
@api.route('/member/', defaults={'id':None})
@api.route('/member/<int:id>', methods=['GET'])
def member_get(id=None):
    member_controller = MemberController()
    if id is None:
        members = member_controller.getMember()
    else:
        print("APIs Route: id = ", id, type(id))
        members = member_controller.getMember(id)
    headers = {"Content-Type": "application/json"}
    print(members[0].to_json())
    return make_response(
        jsonify([member.to_json() for member in members]), 200, headers
    )

@api.route('/member/')
@api.route('/member/<int:id>', methods=['POST'])
def member_post(full_name=None, member_role=None, student_id=None, authorized=False):
    
    member_controller = MemberController()
    result = member_controller.createMember(full_name, member_role, student_id, authorized)
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(result), 200, headers)

@api.route('/member/', defaults={'id':0})
@api.route('/member/<int:id>', methods=['PUT'])
def member_put(id=None):
    member_controller = MemberController()
    member = member_controller.getMember(id)
    return render_template('page/access.html', member=member[0])

@api.route('/member/', defaults={'id':0})
@api.route('/member/<int:id>', methods=['DELETE'])
def member_delete(id=None):
    member_controller = MemberController()
    member = member_controller.getMember(id)
    return render_template('page/access.html', member=member[0])
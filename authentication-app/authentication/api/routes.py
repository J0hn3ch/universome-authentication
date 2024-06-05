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
@api.route('/member/', defaults={'id':None}, methods=['GET'])
@api.route('/member/<int:id>', methods=['GET'])
#@api.route('/member/<string:card_id>', methods=['GET'])
def member_get(id=None):
    member_controller = MemberController()
    if id is None and request.args.get('card_id') is None:
        members = member_controller.getMember()
    elif request.args.get('card_id') is not None:
        print("APIs Route: card_id = ", request.args.get('card_id'), type(request.args.get('card_id')))
        members = member_controller.getMember(card_id=request.args.get('card_id'))
    else:
        print("APIs Route: id = ", id, type(id))
        members = member_controller.getMember(id)
    headers = {"Content-Type": "application/json"}
    print(members[0].to_json())
    return make_response(
        jsonify([member.to_json() for member in members]), 200, headers)

@api.route('/member/', methods=['POST'])
def member_post():
    '''
    POST Request: Register a new member in the database.
    Parameters:
    - full_name
    - member_role
    - student_id
    - authorized


    '''
    print("Request method: %s" % request.method)
    print("URL: %s" % request.url_root)
    print("Path: %s" % request.path)
    print("Request parameters: %s\n" % request.args.to_dict())

    if request.method == 'POST':
        member_controller = MemberController()
        
        result = member_controller.createMember(
            full_name=request.args.get('full_name'),
            member_role=request.args.get('member_role'), 
            student_id=request.args.get('student_id'), 
            authorized=request.args.get('authorized')
        )
        
        headers = {"Content-Type": "application/json"}
        return make_response(jsonify(result), 200, headers)

'''
@api.route('/member/<int:id>', defaults={'id':None}, methods=['PUT'])
def member_put(id, full_name=None, member_role=None, student_id=None, authorized=False):
    #print("PUT - /api/member/" + str(id) if id is not None else "EMPTY")
    if id is None:
        headers = {"Content-Type": "text/plain"}
        return make_response("Please, specify the ID", 500, headers) 
    else:   
        result = {'id' : id, 'full_name' : full_name, 'role' : member_role, 'student_id' : student_id, 'authorized' : authorized}

    #member_controller = MemberController()
    #member = member_controller.getMember(id)
    return make_response(jsonify(result), 200, headers)

@api.route('/member/<int:id>', defaults={'id':None}, methods=['DELETE'])
def member_delete(id=None):
    #print("DELETE - /api/member/" + str(id) if id is not None else "EMPTY")
    if id is None:
        headers = {"Content-Type": "text/plain"}
        return make_response("Please, specify the ID", 500, headers) 
    else:   
        result = {'id' : id}

    #member_controller = MemberController()
    #member = member_controller.getMember(id)
    return make_response(jsonify(result), 200, headers)

'''
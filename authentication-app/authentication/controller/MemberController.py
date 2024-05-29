from authentication.model.MemberModel import Member

class MemberController:
    def __init__(self):
        pass

    def getMember(self, id=None):
        members_list = None
        if id is None:
            # Check if list is empty
            members_list = Member.get_member()
            return members_list
        else:
            print("MemberController: id = ", id, type(id))
            members_list = Member.get_member(member_id=id)
            return members_list
            
        #member_dict = dict(zip(members_list.keys(), members_list))
        #return member_dict
        
        #for member in members_list:
            # member: (id(int), 'Full name', 'Role', 'student_id', 'timestamp', authorized(bool))
    
    def getMemberByChipId(self, chip_id=None):
        member_list = None
        
        if chip_id is None:
            member_list = []
        else:
            member_list = Member.get_member(chip_id=chip_id)
        
        return member_list

    def isAuthorized():
        pass

    def createMember(full_name, member_role, student_id, authorized):
        member = Member(full_name, member_role, student_id, authorized)
        return member.create_member()
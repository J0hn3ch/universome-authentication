from authentication.model.MemberModel import Member

class MemberController:
    def __init__(self):
        pass

    def getMember(self, id=None):
        members_list = None
        print("MemberController: " + str(type(id)))
        if id is None:
            members_list = Member.get_member()
        else:
            members_list = Member.get_member(id)
        
        if not members_list: # Check if list is empty
            return None
        else:
            return members_list
        
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

    


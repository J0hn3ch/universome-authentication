from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from authentication.controller.MemberController import MemberController
from flask_login import login_user, login_required, logout_user

mbr = Blueprint('member', __name__, url_prefix='/')

@mbr.route('/member/', defaults={'chip_id':0})
@mbr.route('/member/<string:chip_id>', methods=['GET', 'POST'])
@login_required
def member(chip_id=None):
    # Get Member by Chip ID | 001122AABB
    if chip_id == 0:
        return "Chip ID is Zero"
    
    member_controller = MemberController()
    member = member_controller.getMemberByChipId(chip_id)
    return render_template('page/access.html', member=member[0])
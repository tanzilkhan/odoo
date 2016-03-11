from openerp.osv import fields, osv
from openerp import tools

class hr_req_blacklist(osv.osv):
    _name='hr.black.list'
    _columns={
        'emp_name':fields.char('Employee Name'),
        'father_name':fields.char('Father Name'),
        'mother_name':fields.char('Mother Name'),
        'mobile_no':fields.char('Mobile Number'),
        'date_of_birth':fields.date('Date Of Birth'),
        'nid':fields.char('National Id'),
    }
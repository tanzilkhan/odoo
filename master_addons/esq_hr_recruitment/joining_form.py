from openerp.osv import fields,osv
from openerp import tools


# class joining_form(osv.osv):
#
#     _name='joining.form'
#
#     _columns={
#         # 'checklist',
#         'joining_date':fields.date('Joining Date'),
#         #joining report,
#         'induction':fields.selection([('a','Yes'),('b', 'No'),],'Induction'),
#         'induction_note':fields.text(),
#         'domain_it_dept':fields.boolean('Email/domain ID to IT Dept'),
#         'security_dept':fields.boolean('ID Card to Security Dept'),
#         'support_service':fields.boolean('Stationary, Lunch to Support Service'),
#     }

class hr_req_joining_form(osv.osv):
    _name='hr.applicant'
    _inherit='hr.applicant'

    _columns={
        'joining_date':fields.date('Joining Date'),
        #joining report,
        'induction':fields.selection([('a','Yes'),('b', 'No'),],'Induction'),
        # 'induction_note':fields.text(),
        'domain_it_dept':fields.boolean('Email/domain ID to IT Dept'),
        'security_dept':fields.boolean('ID Card to Security Dept'),
        'support_service':fields.boolean('Stationary, Lunch to Support Service'),
    }
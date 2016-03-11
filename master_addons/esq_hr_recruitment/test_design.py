from openerp.osv import fields,osv
from openerp import tools


class hr_req_test_design(osv.osv):

    _name='test.design'

    def onchange_recruitment_no(self,cr,uid,ids,recruitment_no,context=None):
        if recruitment_no is not False:
            manpower_get=self.pool.get('manpower.requisition')
            designation=manpower_get.browse(cr,uid,recruitment_no,context=context).job_title.id

            return {'value':{'position':designation}}

        else:
            return {'value':{'position':False}}


    _columns={
        'recruitment_no': fields.many2one('manpower.requisition','Recruitment Number'),
        'position': fields.many2one('hr.job','Position'),
        'exam_type': fields.one2many('test.design.exam','td_rel','Type of Exam'),

        'state': fields.selection([('draft', 'Draft'),('head_hr', 'Head Of HR'), ('approved', 'Approved')], 'Status', readonly=True, required=True,
            help="By default 'In position', set it to 'In Recruitment' if recruitment process is going on for this job position."),
    }

    _defaults ={
        'state':'draft'
    }

    # def job_draft(self, cr, uid, ids, *args):
    #     self.write(cr, uid, ids, {'state': 'recruitment_desk'})
    #     return True

    def create(self, cr, uid, value, context=None ):
        value['state'] = 'head_hr'
        return super(hr_req_test_design, self).create(cr, uid, value, context=context)

    # def job_recruitment_desk(self, cr, uid, ids, *args):
    #     self.write(cr, uid, ids, {'state': 'head_hr'})
    #     return True

    def job_head_hr_approve(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'approved'})
        return True

    def job_head_hr_reject(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'approved'})
        return True

class hr_req_test_design_exam(osv.osv):
    _name='test.design.exam'
    _columns={
        'td_rel':fields.many2one('test.design'),
        'name': fields.many2one('test.design.exam.type', 'Exam Type'),
        'serial_no':fields.integer('Sl No.'),
    }

class hr_req_test_design_exam_type(osv.osv):
    _name='test.design.exam.type'
    _columns={
        'name': fields.char('Exam'),
    }
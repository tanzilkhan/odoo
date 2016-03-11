from openerp.osv import fields, osv
from openerp import tools


class hr_job(osv.osv):


    _inherit='hr.job'

    _columns={
        'question_set':fields.many2one('interview.question.set','Question Set'),
        'job_responsibility':fields.text('Job Responsibility')
    }


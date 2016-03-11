from openerp.osv import fields,osv
from openerp import tools

class hr_interview_question(osv.osv):
    _name='interview.question'
    _columns={
        'name': fields.char('Interview Question'),

    }


class hr_interview_question_rel(osv.osv):
    _name='interview.question.rel'

    _columns={
        'name': fields.many2one('interview.question','Interview Question'),
        'weight':fields.integer('Weight'),
        'rel_qus':fields.many2one('interview.question.set'),

    }


class hr_interview_question_set(osv.osv):
    _name='interview.question.set'



    def create(self,cr,uid,value,context=None):
        total_weight = 0.0
        for each_item in value['question']:
            total_weight = total_weight + each_item[2]['weight']

        if total_weight == value['marks_for_set']:
            return super(hr_interview_question_set, self).create(cr, uid, value, context=context)
        else:
            raise osv.except_osv(('Error!!'),('Not Equal'))

    _columns={
        'name': fields.char('Name Of Question Set'),
        'marks_for_set':fields.float('Marks for This Set'),
        'question':fields.one2many('interview.question.rel','rel_qus','Question'),
    }

class hr_interview_likert_scale(osv.osv):
    _name='interview.likert.scale'
    _columns={
        'name': fields.char('Name'),
        'scale':fields.integer('Scale'),
    }

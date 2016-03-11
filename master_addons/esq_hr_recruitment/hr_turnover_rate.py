from openerp.osv import fields,osv
from openerp import tools
import time
import datetime

class hr_req_turnover_rate(osv.osv):
    _name='hr.turnover.rate'

    def onchange_date(self,cr,uid,ids,current_date,context=None):
        month = datetime.datetime.now().strftime("%m")
        month_list=[]

        existing_employee=self.pool.get('hr.employee').search(cr,uid,[],context=context)

        for i in range(6):
            month_list.append([0,0,{'month': month,'existing_emp':len(existing_employee),'separated_emp':0.0}])
            month=int(month)-1
            month=str(month)

        # month_list.extend()
        # [0,0,{'month': '1'}],[0,0,{'month': '2'}],[0,0,{'month': '3'}]

        return {'value': {'turnover_line':month_list}}

    _columns={
        'average':fields.float('Average'),
        'turnover_rate':fields.float('Turnover Rate'),
        'turnover_line':fields.one2many('hr.turnover.rate.line','td_rel','Turnover Line'),
        'date':fields.date('Date'),
    }

    def _default_date(self, cr, uid, context=None):
        # (time.strftime("%d/%m/%Y"))
        current_date=datetime.date.today().strftime('%Y-%m-%d')
        return current_date

    _defaults={
        # 'turnover_rate':6.0,
        'date': _default_date,

    }

class hr_req_turnover_rate_line(osv.osv):
    _name='hr.turnover.rate.line'
    _columns={
        'month':fields.selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],'Month'),
        'existing_emp':fields.integer('Existing Employees'),
        'separated_emp':fields.integer('Separated Employees'),
        # 'turnover_rate':fields.many2one('hr.turnover.rate','Turnover Rate'),
        'td_rel':fields.many2one('hr.turnover.rate'),
    }
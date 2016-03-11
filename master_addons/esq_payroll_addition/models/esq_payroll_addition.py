import math
from openerp.osv import fields, osv, orm
from openerp import api, tools, SUPERUSER_ID


class officer_staff_addition(osv.Model):
    _inherit = 'hr.employee'
    _columns = {
        'is_officer': fields.boolean('Is Officer'),
        'is_worker': fields.boolean('Is Worker'),
    }

    _defaults = {
        'is_officer': 1,
        'is_staff': 0,
    }

    @api.onchange('is_officer')
    def changing_emp_officer_status(self):
        officer_on = self.is_officer
        if officer_on != 0:
            self.is_worker = 0
        else:
            self.is_worker = 1

    @api.onchange('is_worker')
    def changing_emp_worker_status(self):
        worker_on = self.is_worker
        if worker_on != 0:
            self.is_officer = 0
        else:
            self.is_officer = 1

class contract_addition(osv.Model):
    _inherit = 'hr.contract'
    _columns = {
        'gross_percent': fields.float('Basic % of Gross'),
        'gross_salary': fields.float('Gross Salary')
    }

    @api.onchange('gross_percent','gross_salary')
    def gross_calculation(self):
        gross_p = self.gross_percent
        gross_s = self.gross_salary
        self.wage = gross_s * (gross_p/100)

    # @api.onchange('wage','gross_percent')
    # def basic_calculation(self):
    #     basic = self.wage
    #     gross_pc = self.gross_percent
    #     if gross_pc == 0:
    #         self.gross_salary = 0
    #     else:
    #         self.gross_salary = (basic*100)/gross_pc
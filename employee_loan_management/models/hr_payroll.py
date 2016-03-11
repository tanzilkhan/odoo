# -*- coding: utf-8 -*-
# © 2016 MD Tanzilul Hasan Khan (<http://www.tanzilkhan.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.osv import osv


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    @api.one
    def compute_total_paid_loan(self):
        totalAS = 0.00
        totalCL = 0.00
        totalEL = 0.00
        totalPL = 0.00
        for line in self.loan_ids:
            if line.loan_type == 'advance_salary':
                if line.paid == True:
                    totalAS += line.paid_amount
            elif line.loan_type == 'car_loan':
                if line.paid == True:
                    totalCL += line.paid_amount
            elif line.loan_type == 'eips_loan':
                if line.paid == True:
                    totalEL += line.paid_amount
            elif line.loan_type == 'pf_loan':
                if line.paid == True:
                    totalPL += line.paid_amount

        self.total_amount_paid = totalAS
        self.total_amount_paid_cl = totalCL
        self.total_amount_paid_el = totalEL
        self.total_amount_paid_pl = totalPL

    loan_ids = fields.One2many('hr.loan.line', 'payroll_id', string="Loans")
    total_amount_paid = fields.Float(string="Total Advance Loan Amount", compute='compute_total_paid_loan')
    total_amount_paid_cl = fields.Float(string="Total Car Loan Amount", compute='compute_total_paid_loan')
    total_amount_paid_el = fields.Float(string="Total EIPS Loan Amount", compute='compute_total_paid_loan')
    total_amount_paid_pl = fields.Float(string="Total PF Loan Amount", compute='compute_total_paid_loan')

    # @api.multi
    # def get_loan(self):
    #     array = []
    #     loan_ids = self.env['hr.loan.line'].search([('employee_id', '=', self.employee_id.id), ('paid', '=', False)])
    #     for loan in loan_ids:
    #         print '***********'
    #         print loan.paid_date
    #         print '***********'
    #         array.append(loan.id)
    #     self.loan_ids = array
    #     return array

    @api.multi
    @api.model
    def compute_sheet(self):
        for i in self:
            array = []
            loan_ids = self.env['hr.loan.line'].search([('employee_id', '=', i.employee_id.id), ('paid', '=', False)])
            for loan in loan_ids:
                array.append(loan.id)
            i.loan_ids = array

            for lo in i.loan_ids:
                if lo.paid_date >= i.date_from and lo.paid_date <= i.date_to:
                    lo.paid = True
                computation = super(hr_payslip, i).compute_sheet()
        return computation

    # @api.multi
    # def get_loan(self):
    #
    #     for lo in self.loan_ids:
    #         if lo.paid_date >= self.date_from and lo.paid_date <= self.date_to:
    #             lo.paid = True
    #     # return self.loan_ids.paid

    @api.model
    def hr_verify_sheet(self):
        self.compute_sheet()
        array = []
        for line in self.loan_ids:
            if line.paid:
                array.append(line.id)
                line.action_paid_amount()
            else:
                line.payroll_id = False
        self.loan_ids = array
        return self.write({'state': 'verify'})

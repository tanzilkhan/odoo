# -*- coding: utf-8 -*-
# © 2016 MD Tanzilul Hasan Khan (<http://www.tanzilkhan.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

LOAN_TYPE_SELECTION = [
    ('advance_salary','Advance Salary'),
    ('car_loan','Car Loan'),
    ('eips_loan','Eips Loan'),
    ('pf_loan','Provident Fund Loan'),
]

class hr_loan(models.Model):
    _name = 'hr.loan'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _description= "HR Loan Request"


    @api.one
    def _compute_amount(self):
        total_paid_amount = 0.00
        loan_calc_amount = 0.00
        for loan in self:
            for line in loan.loan_line_ids:
                if line.paid == True:
                    total_paid_amount +=line.paid_amount
                else:
                    loan_calc_amount += line.paid_amount

            balance_amount = loan_calc_amount - total_paid_amount
            self.total_amount = loan_calc_amount
            self.balance_amount = balance_amount
            self.total_paid_amount = total_paid_amount



    @api.one
    def _get_old_loan(self):
        old_amount = 0.00
        for loan in self.search([('employee_id','=',self.employee_id.id)]):
            if loan.id != self.id:
                old_amount += loan.balance_amount
        self.loan_old_amount = old_amount

    name = fields.Char(string="Loan Name", default="/", readonly=True)
    date = fields.Date(string="Date Request", default=fields.Date.today(), readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    parent_id = fields.Many2one('hr.employee', related= "employee_id.parent_id", string="Manager")
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True, string="Department")
    job_id = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position")
    emp_salary = fields.Float(string="Employee Salary",related="employee_id.contract_id.wage", readonly=True)
    loan_old_amount = fields.Float(string="Old Loan Amount Not Paid", compute='_get_old_loan')
    emp_account_id = fields.Many2one('account.account', string="Employee Account", readonly=True)
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account")
    journal_id = fields.Many2one('account.journal', string="Journal")
    loan_amount = fields.Float(string="Loan Amount", required=True)
    total_amount = fields.Float(string="Total Amount", readonly=True, compute='_compute_amount')
    balance_amount = fields.Float(string="Balance Amount", compute='_compute_amount')
    total_paid_amount = fields.Float(string="Total Paid Amount", compute='_compute_amount')
    no_month = fields.Integer(string="No Of Month", default=1)
    payment_start_date = fields.Date(string="Start Date of Payment", required=True, default=fields.Date.today())
    loan_line_ids = fields.One2many('hr.loan.line', 'loan_id', string="Loan Line", index=True)
    entry_count = fields.Integer(string="Entry Count", compute = 'compute_entery_count')
    move_id = fields.Many2one('account.move', string="Entry Journal", readonly=True)
    #Added by Tanzil
    loan_type = fields.Selection(LOAN_TYPE_SELECTION, string="Loan Type", default='advance_salary',)
    interest = fields.Float('Interest Rate (%)')
    interest_bool = fields.Boolean('Has Interest')
    # loan_types = fields.Char(string='Loan Type')

    #State modified by Tanzil
    state = fields.Selection([
        ('draft','Draft'),
        ('hod','HOD Approval'),
        ('hr','HR Approval'),
        ('finance','Finance Approval'),
        ('md','MD Approval'),
        ('approve','Approved'),
        ('refuse','Refused'),
    ], string="State", default='draft', track_visibility='onchange', copy=False,)


    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].get('hr.loan.req') or ' '
        res = super(hr_loan, self).create(values)
        return res

    @api.one
    def action_refuse(self):
        self.state = 'refuse'


    @api.one
    def action_set_to_draft(self):
        self.state = 'draft'

    #Extra buttons for esquire by Tanzil
    @api.one
    def action_set_to_hod(self):
        self.state = 'hod'

    @api.one
    def action_set_to_hr(self):
        self.state = 'hr'

    @api.one
    def action_set_to_finance(self):
        self.state = 'finance'

    @api.one
    def action_set_to_md(self):
        self.state = 'md'
        if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
            raise except_orm('Warning', "You must enter employee account & Treasury account and journal to approve ")
        if not self.loan_line_ids:
            raise except_orm('Warning', 'You must compute Loan Request before Approved')

    #Added by Tanzil
    @api.onchange('loan_type')
    def loan_type_change(self):
        if self.loan_type != 'advance_salary':
            self.interest = 0.00

    @api.onchange('interest_bool')
    def loan_interest_state_change(self):
        if self.interest_bool != True:
            self.interest = 0.00

    @api.multi
    def onchange_employee_id(self, employee_id=False):
        old_amount = 0.00
        if employee_id:
            for loan in self.search([('employee_id','=',employee_id)]):
                if loan.id != self.id:
                    old_amount += loan.balance_amount
            return {
                'value':{
                    'loan_old_amount':old_amount}
            }

    @api.one
    def action_approve(self):
        self.state = 'approve'
        # modified by tanzil
        # if not self.emp_account_id or not self.treasury_account_id or not self.journal_id:
        #     raise except_orm('Warning', "You must enter employee account & Treasury account and journal to approve ")
        # if not self.loan_line_ids:
        #     raise except_orm('Warning', 'You must compute Loan Request before Approved')
        can_close = False
        loan_obj = self.env['hr.loan']
        period_obj = self.env['account.period']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        currency_obj = self.env['res.currency']
        created_move_ids = []
        loan_ids = []
        for loan in self:
            loan_request_date = loan.date
            period_ids =period_obj.with_context().find(loan_request_date).id
            company_currency = loan.employee_id.company_id.currency_id.id
            current_currency = self.env.user.company_id.currency_id.id
            amount = loan.loan_amount
            loan_name = loan.employee_id.name
            reference = loan.name
            journal_id = loan.journal_id.id
            move_vals = {
                'name': loan_name,
                'date': loan_request_date,
                'ref': reference,
                'period_id': period_ids or False,
                'journal_id': journal_id,
                'state': 'posted',
                }
            move_id = move_obj.create(move_vals)
            move_line_vals = {
                'name': loan_name,
                'ref': reference,
                'move_id': move_id.id,
                'account_id': loan.treasury_account_id.id,
                'debit': 0.0,
                'credit': amount,
                'period_id': period_ids or False,
                'journal_id': journal_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency':  0.0,
                'date': loan_request_date,
            }
            move_line_obj.create(move_line_vals)
            move_line_vals2 = {
                'name': loan_name,
                'ref': reference,
                'move_id': move_id.id,
                'account_id': loan.emp_account_id.id,
                'credit': 0.0,
                'debit': amount,
                'period_id': period_ids or False,
                'journal_id': journal_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': 0.0,
                'date': loan_request_date,
            }
            move_line_obj.create(move_line_vals2)
            self.write({'move_id': move_id.id})
        return True



    @api.multi
    def compute_loan_line(self):
        loan_line = self.env['hr.loan.line']
        loan_line.search([('loan_id','=',self.id)]).unlink()
        for loan in self:
            date_start_str = datetime.strptime(loan.payment_start_date,'%Y-%m-%d')
            counter = 1
            # amount_per_time = loan.loan_amount / loan.no_month
            # if self.loan_type == 'advance_salary' or self.loan_type == 'pf_loan':
            if self.interest_bool == True:
                if self.interest > 0.00:
                    loan_amount = float(self.loan_amount)
                    numberOfPayments = float(self.no_month)
                    interest = float(self.interest)/100/12
                    amount_pmt = loan_amount * (interest * (1 + interest) ** numberOfPayments) / ((1 + interest) ** numberOfPayments - 1)
                    amount_per_time = amount_pmt
                else:
                    raise except_orm('Warning', 'Interest rate cannot be 0.00 (zero)')
            else:
                amount_per_time = loan.loan_amount / loan.no_month
            for i in range(1, loan.no_month + 1):
                line_id = loan_line.create({
                    'paid_date':date_start_str,
                    'paid_amount': amount_per_time,
                    'employee_id': loan.employee_id.id,
                    'loan_type':loan.loan_type,
                    'loan_id':loan.id})
                counter += 1
                date_start_str = date_start_str + relativedelta(months = 1)

        return True


    @api.model
    @api.multi
    def compute_entery_count(self):
        count = 0
        for i in self:
            entry_count = self.env['account.move.line'].search_count([('loan_id','=',i.id)])
            i.entry_count = entry_count

    @api.multi
    def button_reset_balance_total(self):
        total_paid_amount = 0.00
        for loan in self:
            for line in loan.loan_line_ids:
                if line.paid == True:
                    total_paid_amount +=line.paid_amount
            balance_amount =loan.loan_amount - total_paid_amount
            self.write({'total_paid_amount':total_paid_amount,'balance_amount':balance_amount})


class hr_loan_line(models.Model):
    _name="hr.loan.line"
    _description = "HR Loan Request Line"


    paid_date = fields.Date(string="Payment Date", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    paid_amount = fields.Float(string="Paid Amount", required=True)
    paid = fields.Boolean(string="Paid")
    notes = fields.Text(string="Notes")
    loan_id = fields.Many2one('hr.loan', string="Loan Ref.", ondelete='cascade')
    payroll_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
    # loan_types = fields.Char(string='Loan Type')
    loan_type = fields.Selection(LOAN_TYPE_SELECTION, type='selection', string='Loan Type')


    @api.one
    def action_paid_amount(self):
        context = self._context
        can_close = False
        loan_obj = self.env['hr.loan']
        period_obj = self.env['account.period']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        currency_obj = self.env['res.currency']
        created_move_ids = []
        loan_ids = []
        for line in self:
            if line.loan_id.state != 'approve':
                raise except_orm('Warning', "Loan Request must be approved")
            paid_date = line.paid_date
            period_ids =period_obj.with_context().find(paid_date).id
            company_currency = line.employee_id.company_id.currency_id.id
            current_currency = self.env.user.company_id.currency_id.id
            amount = line.paid_amount
            loan_name = line.employee_id.name
            reference = line.loan_id.name
            journal_id = line.loan_id.journal_id.id
            move_vals = {
                'name': loan_name,
                'date': paid_date,
                'ref': reference,
                'period_id': period_ids or False,
                'journal_id': journal_id,
                'state': 'posted',
                }
            move_id = move_obj.create(move_vals)
            move_line_vals = {
                'name': loan_name,
                'ref': reference,
                'move_id': move_id.id,
                'account_id': line.loan_id.emp_account_id.id,
                'debit': 0.0,
                'credit': amount,
                'period_id': period_ids or False,
                'journal_id': journal_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency':  0.0,
                'date': paid_date,
                'loan_id':line.loan_id.id,
            }
            move_line_obj.create(move_line_vals)
            move_line_vals2 = {
                'name': loan_name,
                'ref': reference,
                'move_id': move_id.id,
                'account_id': line.loan_id.treasury_account_id.id,
                'credit': 0.0,
                'debit': amount,
                'period_id': period_ids or False,
                'journal_id': journal_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': 0.0,
                'date': paid_date,
                'loan_id':line.loan_id.id,
            }
            move_line_obj.create(move_line_vals2)
            self.write({'paid': True})
        return True




class hr_employee(models.Model):
    _inherit = "hr.employee"

    @api.model
    @api.multi
    def _compute_loans(self):
        for i in self:
            count = 0
            loan_remain_amount = 0.00
            loan_ids = self.env['hr.loan'].search([('employee_id','=',i.id)])
            for loan in loan_ids:
                loan_remain_amount +=loan.balance_amount
                count +=1
            i.loan_count = count
            i.loan_amount = loan_remain_amount
            break



    loan_amount= fields.Float(string="loan Amount", compute ='_compute_loans')
    loan_count = fields.Integer(string="Loan Count", compute = '_compute_loans')


class account_move_line(models.Model):
    _inherit = "account.move.line"

    loan_id = fields.Many2one('hr.loan', string="Loan")

class loan_type_var(models.Model):
    _name = "hr.loan.type"

    loan_type = fields.Char('Name',)
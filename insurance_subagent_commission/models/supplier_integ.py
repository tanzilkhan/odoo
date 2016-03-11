# -*- coding: utf-8 -*-
# © 2016 MD Tanzilul Hasan Khan (<http://www.tanzilkhan.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
import datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning


class supplier_on_customer(models.Model):
    _inherit = "res.partner"

    suppliers_on_cus = fields.Many2many(
        comodel_name="res.partner", relation="partner_supplier_rel",
        column1="partner_id", column2="supplier_id",
        domain="[('supplier', '=', 'True')]")


class commission_computation_model(models.Model):
    _inherit = 'hr.employee'

    @api.model
    @api.multi
    def _compute_commissions(self):
        # count = 0
        loan_remain_amount = 0.00
        loan_ids = self.env['res.partner'].search([('sub_agents', '=', self.id)])
        for i in loan_ids:
            loan_remain_amount += i.total_gross
            # count +=1
        # self.loan_count = count
        self.total_gross = loan_remain_amount

    @api.multi
    @api.depends('total_gross', 'gross_paid')
    def _unpaid_amount(self):
        self.gross_unpaid = self.total_gross - self.gross_paid

    total_gross = fields.Float(string='Total Gross Commission', compute='_compute_commissions')
    is_a_agent = fields.Boolean(string='Is Agent')
    gross_paid = fields.Float(string='Total Paid Gross Commission', readonly=True, store=True)
    gross_unpaid = fields.Float(string='Total Unpaid Gross Commission', compute='_unpaid_amount')
    percent_gunpaid = fields.Float(string='Percentage to be Paid %')
    pay_amount = fields.Float(string='Last Payable Commission',
                              help='This amount will be paid through payslip based on Payment Generation Date')
    payment_date = fields.Date(string='Payment Generation Date',
                               help='This date will determine one which month the agent will be paid')
    paid_to_agent = fields.Float(string='Total Paid to Agent')
    pmt_amount = fields.Float(string='Pay Amount')
    calculation_summary = fields.Text(string='Summary', readonly=True)
    generate_clicked = fields.Boolean('Generate Mark')

    # agent commission lines
    agent_commission_line = fields.One2many(comodel_name='agent.commission.line', inverse_name='name',
                                            string='Agent Commission Details')

    @api.multi
    def button_compute_commission(self):
        if self.pmt_amount <= self.gross_unpaid:
            gross_paid = self.gross_paid + self.pmt_amount
            payment_date = datetime.datetime.now().strftime("%m-%d-%y")
            pay_amount = self.pmt_amount * (self.percent_gunpaid/100)
            paid_to_agent = self.paid_to_agent + self.pay_amount
            self.calculation_summary = 'Based on '+str(self.pmt_amount)+' gross amount ' +\
                                       'Latest payment amount will be ' + str(pay_amount) +'\n\n'+ \
                                       'This amount will be paid in the month of this date: '+str(payment_date)+'\n\n'+\
                                       'Total Paid Gross Amount will be: '+str(gross_paid)+'\n'+\
                                       'Total Amount Paid to the Agent will be '+str(paid_to_agent)
            self.generate_clicked = True
            return True
        else:
            raise except_orm('Warning', "Payment amount cannot be higher than the unpaid amount")

    @api.multi
    def button_confirm_commission(self):
            self.gross_paid = self.gross_paid + self.pmt_amount
            self.payment_date = datetime.datetime.now()
            self.pay_amount = self.pmt_amount * (self.percent_gunpaid/100)
            self.paid_to_agent = self.paid_to_agent + self.pay_amount
            self.calculation_summary = None
            self.generate_clicked = False
            return True

    @api.multi
    def button_clear(self):
        self.calculation_summary = None
        self.generate_clicked = False
        return True

class agent_commission_line(models.Model):
    _name = 'agent.commission.line'

    @api.multi
    @api.depends('commission_percent', 'sales_amount')
    def commission_earned_calculation(self):
        self.commission_earned = self.sales_amount * (self.commission_percent / 100)

    name = fields.Many2one('hr.employee', 'Name')
    agent_rel = fields.Many2one('hr.employee', string='Sub-Agent', readonly=True)
    customer_agent_rel = fields.Many2one('res.partner', string='Customer', readonly=True)
    date_invoice = fields.Date(string='Date', readonly=True)
    sales_amount = fields.Float(string='Sales Amount', readonly=True)
    commission_percent = fields.Float(string='Commission Percent (%)', readonly=True)
    commission_earned = fields.Float(string='Commission Earned', compute='commission_earned_calculation',
                                     readonly=True, store=True)

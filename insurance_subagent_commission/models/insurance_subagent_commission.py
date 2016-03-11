# -*- coding: utf-8 -*-
# © 2016 MD Tanzilul Hasan Khan (<http://www.tanzilkhan.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.osv import osv, fields, orm
from openerp import api


class customer_edit(osv.osv):
    _inherit = 'res.partner'

    @api.one
    @api.depends('customer_status.gross_commission')
    def _compute_gross_amount(self):
        self.total_gross = sum(line.gross_commission for line in self.customer_status)

    _columns = {
        'ins_suppliers': fields.one2many('res.partner', 'name', 'Suppliers'),
        'cus_acc_type': fields.selection([('personal', 'Personal'), ('corporate', 'Corporate'),
                                          ('subagent', 'Sub-Agent')], 'Account Type', ),

        # product page fields
        'customer_status': fields.one2many('customer.product.status', 'name', 'Customer Product Status'),
        'product_remarks': fields.text('Remarks'),

        # Related with agent commission payment
        'total_gross': fields.float('Total Gross Commission', store=True, readonly=True,
                                    compute='_compute_gross_amount', ),
        'sub_agents': fields.many2one('hr.employee', 'Sub-agents')
    }


class customer_product_status(osv.Model):
    _name = 'customer.product.status'

    @api.one
    @api.depends('premium_paid', 'commission_pcnt')
    def _premium_change_comm(self):
        commission_percent = self.commission_pcnt / 100
        self.gross_commission = self.premium_paid * commission_percent

    _columns = {
        'name': fields.char('Customer Status'),
        'status': fields.selection([('lapsed', 'Lapsed'), ('active', 'Active')], 'Status', ),
        'renewal_due': fields.selection([('inactive', 'Inactive'), ('renewal_thirty', 'Renewal>30 Days'),
                                         ('renewal_thirty_ex', 'Renewal<30 Days'), ],
                                        'Renewal Due (<30 Days from Policy End)'),
        'policy_start': fields.date('Policy Start'),
        'policy_end': fields.date('Policy End'),
        # 'type_of_insurance': fields.many2one('insurance.type', 'Insurance Type'),
        'premium_paid': fields.float('Premium Paid without GST'),
        'commission_pcnt': fields.float('Commission Percentage'),
        'gross_commission': fields.float('Gross Commission', store=True, compute='_premium_change_comm'),
        'policy_number': fields.char('Policy Number'),
        'current_payment': fields.selection([('collected', 'Collected')], 'Current Payment'),
        'ins_remarks': fields.text('Remarks'),
        'suppliers_on_policy': fields.many2one('res.partner', domain="[('supplier', '=', 'True')]",
                                               string='Insurance Company'),
        'customer_related': fields.many2one('res.partner', 'Customers'),
        'date_created': fields.date('Date Created'),
        'type_of_insurance': fields.selection([('travelon', 'Travelon'), ('fwmp', 'Foreign Workers Medical Plan'),
                                          ('marine_hull', 'Marine Hull'), ('home_plus', 'Home Plus Cover'),
                                          ('annual_travel_std', 'Annual Travel - Std. Ap'),
                                          ('annual_travel_world', 'Annual Travel - Std. Worldwide'),
                                          ('burglary', 'Burglary'),('building_content', 'Building Content'),
                                          ('commercial_fire', 'Commercial Fire'), ('commercial_pac', 'Commercial Package'),
                                          ('contractor_pl_eq', 'Contractor Plant & Equipment'), ('fire', 'Fire'),
                                          ('fidelity_gur', 'Fidelity Guarantee'), ('health', 'Health'), ('home', 'Home'),
                                          ('imm_bond', 'Immigration Bond / Other Bonds'),
                                          ('individual_travel_std', 'Individual Travel - Std. Ap'),
                                          ('individual_travel_world', 'Individual Travel - Std. Worldwide'),
                                          ('lost_profit', 'Lost of Profit'), ('machinery', 'Machinery'),
                                          ('marine_cargo', 'Marine Cargo'), ('money', 'Money'), ('motor', 'Motor'),
                                          ('perf_sec_bond', 'Performance / Security Bond'),
                                          ('personal_acc', 'Personal Accident'), ('pleasure_craft', 'Pleasure Craft'),
                                          ('public_liab', 'Public Liability'),
                                          ('prod_oth_liab', 'Product and Other Liabilities'), ('wica', 'WICA'),
                                          ],
                                         'Insurance Type',),
    }


class insurance_type(osv.Model):
    _name = 'insurance.type'
    _columns = {
        'name': fields.char('Insurance Type'),
    }


class account_invoice_mod(osv.Model):
    _inherit = 'account.invoice'

    @api.multi
    @api.depends('partner_id')
    def _agent_populate_partner_id(self):
        if self.partner_id:
            p = self.env['res.partner'].browse([self.partner_id.id])
            self.sub_agents = p.sub_agents.id

    _columns = {
        'invoice_for': fields.selection([('new', 'New'), ('renewal', 'Renewal'), ('additional', 'Additional')],
                                        'Invoice For    '),
        'policy_class': fields.selection([('travelon', 'Travelon'), ('fwmp', 'Foreign Workers Medical Plan'),
                                          ('marine_hull', 'Marine Hull'), ('home_plus', 'Home Plus Cover'),
                                          ('annual_travel_std', 'Annual Travel - Std. Ap'),
                                          ('annual_travel_world', 'Annual Travel - Std. Worldwide'),
                                          ('burglary', 'Burglary'),('building_content', 'Building Content'),
                                          ('commercial_fire', 'Commercial Fire'), ('commercial_pac', 'Commercial Package'),
                                          ('contractor_pl_eq', 'Contractor Plant & Equipment'), ('fire', 'Fire'),
                                          ('fidelity_gur', 'Fidelity Guarantee'), ('health', 'Health'), ('home', 'Home'),
                                          ('imm_bond', 'Immigration Bond / Other Bonds'),
                                          ('individual_travel_std', 'Individual Travel - Std. Ap'),
                                          ('individual_travel_world', 'Individual Travel - Std. Worldwide'),
                                          ('lost_profit', 'Lost of Profit'), ('machinery', 'Machinery'),
                                          ('marine_cargo', 'Marine Cargo'), ('money', 'Money'), ('motor', 'Motor'),
                                          ('perf_sec_bond', 'Performance / Security Bond'),
                                          ('personal_acc', 'Personal Accident'), ('pleasure_craft', 'Pleasure Craft'),
                                          ('public_liab', 'Public Liability'),
                                          ('prod_oth_liab', 'Product and Other Liabilities'), ('wica', 'WICA'),
                                          ],
                                         'Policy Class', required=1),
        'policy_no': fields.char('Policy No.'),
        'ins_date_from': fields.date('Date From'),
        'ins_date_to': fields.date('Date to'),
        'sub_agents': fields.many2one('hr.employee', 'Sub-agents', compute='_agent_populate_partner_id',
                                      store=True),
        'agent_commission': fields.float('Gross Commission (%)'),

        # Travelon
        'insured_person': fields.one2many('insured.person.line', 'name', 'Insured Person'),
        'area': fields.char('Area'),
        'plan_covered': fields.many2one('plan.covered.line', 'Plan Covered'),
        'benefit_travelon': fields.char('Benefits'),

        # Foreign Workers Medical
        'interest_fwmp': fields.float('Interest'),
        'plan_type': fields.many2one('plan.type.line', 'Plan Type'),
        'benefit_fwmp': fields.char('Benefits'),

        # Marine Hull
        'interest_mh': fields.float('Interest'),
        'vessel_des': fields.char('Vessel Description'),
        'vessel_no': fields.char('Vessel No.'),
        'vessel_name': fields.char('Vessel Name'),
        'cover_type': fields.many2one('cover.type.line', 'Type of Cover'),
        'limit_of_liab': fields.char('Vessel Name'),

        # Home Plus Covered
        'sit_at_risk': fields.char('Situation at Risk'),
        'interest_hpc': fields.float('Interest'),
        'sum_insured': fields.char('Sum Insured'),

        # Description for other policies
        'policy_description': fields.text('Polcy Description'),
    }

    @api.multi
    def invoice_validate(self):
        # Customer Status update starts here
        customer_obj = self.env['res.partner']
        customer_id = customer_obj.search([('id','=',self.partner_id.id)])
        customer_line = customer_obj.browse([customer_id.id])
        dd = {
            'policy_number': self.policy_no,
            'policy_start': self.ins_date_from,
            'policy_end': self.ins_date_to,
            'customer_related': self.partner_id.id,
            'premium_paid': self.amount_untaxed,
            'commission_pcnt': self.agent_commission,
            'date_created': self.date_invoice,
            'type_of_insurance': self.policy_class,
        }
        customer_stat_add = customer_line.write({
            'sub_agents': self.sub_agents.id,
            'customer_status': [(0, 0, dd)]
        })

        # Agent Commission Earnings passing to agent form starts here
        agent_obj = self.env['hr.employee']
        agent_id = agent_obj.search([('id','=',self.sub_agents.id)])
        agent_line = agent_obj.browse([agent_id.id])
        agent_line_values = {
            'agent_rel': self.sub_agents.id,
            'customer_agent_rel': self.partner_id.id,
            'date_invoice': self.date_invoice,
            'sales_amount': self.amount_untaxed,
            'commission_percent': self.agent_commission,
        }
        agent_stat_add = agent_line.write({
            'agent_commission_line': [(0, 0, agent_line_values)]
        })

        res = super(account_invoice_mod, self).invoice_validate()

        return customer_stat_add, agent_stat_add, res

class policy_class_line(osv.Model):
    _name = 'policy.class.line'
    _columns = {
        'name': fields.char('Policy Class'),
    }


class cover_type_line(osv.Model):
    _name = 'cover.type.line'
    _columns = {
        'name': fields.char('Type of Cover'),
    }


class plan_tupe_line(osv.Model):
    _name = 'plan.type.line'
    _columns = {
        'name': fields.char('Plan Type'),
    }


class plan_covered_line(osv.Model):
    _name = 'plan.covered.line'
    _columns = {
        'name': fields.char('Plan Covered'),
    }


class insured_person_line(osv.Model):
    _name = 'insured.person.line'
    _columns = {
        'name': fields.many2one('account.invoice', 'Insured Person'),
        'insured_person_name': fields.char('Insured Person'),
    }


class product_tempalte_mod(osv.Model):
    _inherit = 'product.template'
    _columns = {
        'type_of_insurance': fields.many2one('insurance.type', 'Insurance Type'),
    }

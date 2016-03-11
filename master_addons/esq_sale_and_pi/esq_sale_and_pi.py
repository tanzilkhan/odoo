from openerp.osv import osv, fields, orm
from openerp import api, tools, SUPERUSER_ID
from num2words import num2words

class terms_conditions(osv.Model):
    _name = 'terms.conditions'
    _description = ''
    _columns = {
        'name': fields.char('Terms & Condition', size=30),
        'is_on': fields.boolean('Active'),
        'tc_description': fields.text('Description'),
    }

class retailer_desc(osv.Model):
    _name = 'retailer.desc'
    _description = ''
    _columns = {
        'name': fields.char('Retailer Name'),
        'retailer_code': fields.char('Retailer Code'),
        'is_size': fields.boolean('Has Size'),
        'size_details': fields.one2many('account.invoice.line','name','Size Details')
    }

class size_details_line(osv.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    _description = ''

    # def default_get(self, cr, uid, ids, context):
        # res = {}
        # if context:
        #     context_keys = context.keys()
        #     next_sequence = 1
        #     if 'invoice_line' in context_keys:
        #         if len(context.get('invoice_line')) > 0:
        #             next_sequence = len(context.get('invoice_line')) + 1
        # res.update({'sequence_no': next_sequence})
        # return res


    _columns = {
        # 'sequence_no':fields.integer('Sequence',default='1'),
        'euro_size': fields.many2one('retailer.euro.size','Euro Size', size=30),
        'uk_size': fields.many2one('retailer.uk.size','UK Size', size=30),
        'cn_size': fields.many2one('retailer.cn.size','CN Size', size=30),
        'size':fields.many2one('retailer.size','Size', size=30),
        'color_pan': fields.many2one('retailer.color.pan','Color/Pantone', size=30),
        'retailer_size': fields.boolean('Size Check'),
    }


class retailer_euro_size(osv.Model):
    _name = 'retailer.euro.size'
    _columns = {
        'name': fields.text('Euro Size', size=30),
    }

class retailer_uk_size(osv.Model):
    _name = 'retailer.uk.size'
    _columns = {
        'name': fields.text('UK Size', size=30),
    }

class retailer_cn_size(osv.Model):
    _name = 'retailer.cn.size'
    _columns = {
        'name': fields.text('CN Size', size=30),
    }


class retailer_size(osv.Model):
    _name = 'retailer.size'
    _columns = {
        'name': fields.text('Size', size=30),
    }

class retailer_color_pan(osv.Model):
    _name = 'retailer.color.pan'
    _columns = {
        'name': fields.text('Color/Pantone', size=30),
    }

class customer_addition(osv.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _columns = {
        'shipping_name': fields.char('Name'),
        'shipping_address': fields.char('Address'),
        'shipping_mobile': fields.integer('Mobile'),
    }

class retailer_info_invoice(osv.Model):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('other_cost.cost_amount', 'invoice_line.price_subtotal')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.total_other_cost = sum(line.cost_amount for line in self.other_cost)
        self.amount_total = self.amount_untaxed + self.total_other_cost

    @api.one
    @api.depends('amount_total', 'total_other_cost')
    def _total_to_words(self):
        total = self.amount_total
        total_word = num2words(total)
        self.amount_total_words = total_word.upper()


    _columns = {
        'retailer_name': fields.many2one('retailer.desc', 'Retailer'),
        'style_no': fields.char('Style No.'),
        'ebiz_no': fields.char('eBiz So No.'),
        'po_no': fields.char('Po No.'),
        'goodsr_date': fields.date('Goods Ready Date'),
        'hs_code': fields.char('HS Code'),
        'terms_conditions': fields.many2one('terms.conditions', 'T&C to Apply'),
        'termscond_description': fields.text('TERMS & CONDITION'),
        'amount_total_words': fields.char('In Words', compute='_total_to_words', store=True, readonly='True'),
        'has_size': fields.boolean('Size Check'),
        'pi_no':fields.char('PI No'),
        'other_cost':fields.one2many('other.cost.line', 'name', 'Other Cost'),
        'total_other_cost': fields.float('Other Cost Total', store=True, compute='_compute_amount',),
    }

    _sql_constraints = [
        ('pi_no_uniq', 'UNIQUE(pi_no)', 'The PI number must be unique!'),
    ]

    @api.one
    @api.onchange('terms_conditions')
    def onchange_terms_conditions(self):
        new_var=self.terms_conditions.id
        self.termscond_description = self.env['terms.conditions'].browse(new_var).tc_description


    @api.one
    @api.depends('amount_total', 'total_other_cost')
    def _total_to_words(self):
        total = self.amount_total
        total_word = num2words(total)
        self.amount_total_words = total_word.upper()

    @api.onchange('retailer_name')
    def retailer_change(self):
        retailer = self.retailer_name.id
        pi_no=self.env['retailer.desc'].browse(retailer).retailer_code
        size_check = self.env['retailer.desc'].browse(retailer).is_size
        if size_check == True:
            self.has_size = True
        else:
            self.has_size = False
        self.pi_no = pi_no

    # @api.onchange('other_cost')
    # def other_cost_change(self):
    #     cost = self.other_cost
    #     self.amount_total = self.amount_total+cost

    # @api.one
    # @api.depends('other_cost.cost_amount')
    # def _compute_amount(self):
    #     self.total_other_cost = sum(line.cost_amount for line in self.other_cost)


class other_cost_line(osv.Model):
    _name = 'other.cost.line'
    _columns = {
        'name': fields.many2one('account.invoice', 'Name'),
        'other_costs': fields.many2one('other.costs.list', 'Other Costs'),
        'cost_amount': fields.float('Amount'),
    }

class other_cost_list(osv.Model):
    _name = 'other.costs.list'
    _columns = {
        'name': fields.char('Other Cost Name'),
    }
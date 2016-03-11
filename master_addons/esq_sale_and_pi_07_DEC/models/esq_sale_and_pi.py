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
    _columns = {
        'euro_size': fields.many2one('retailer.euro.size','Euro Size', size=30),
        'uk_size': fields.many2one('retailer.uk.size','UK Size', size=30),
        'cn_size': fields.many2one('retailer.cn.size','CN Size', size=30),
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
    _columns = {
        'retailer_name': fields.many2one('retailer.desc', 'Retailer'),
        'style_no': fields.char('Style No.'),
        'ebiz_no': fields.char('eBiz So No.'),
        'po_no': fields.char('PO No.'),
        'goodsr_date': fields.date('Goods Ready Date'),
        'hs_code': fields.char('HS Code'),
        'terms_conditions': fields.many2one('terms.conditions', 'T&C to Apply'),
        'termscond_description': fields.text('TERMS & CONDITION'),
        'amount_total_words': fields.char('In Words'),
        'has_size': fields.boolean('Size Check'),
        'other_cost':fields.float('Other Cost'),
    }

    @api.one
    @api.onchange('terms_conditions')
    def onchange_terms_conditions(self):
        new_var=self.terms_conditions.id
        self.termscond_description = self.env['terms.conditions'].browse(new_var).tc_description


    @api.onchange('amount_total', 'amount_tax')
    def total_to_words(self):
        total = self.amount_total
        total_word = num2words(total)
        self.amount_total_words = total_word.upper()

    @api.onchange('retailer_name')
    def retailer_change(self):
        retailer = self.retailer_name.id
        size_check = self.env['retailer.desc'].browse(retailer).is_size
        if size_check == True:
            self.has_size = True
        else:
            self.has_size = False

    @api.onchange('other_cost')
    def other_cost_change(self):
        cost = self.other_cost
        self.amount_total = self.amount_total+cost

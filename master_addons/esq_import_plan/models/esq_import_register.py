from openerp.osv import osv, fields, orm
from openerp import api

import openerp.addons.decimal_precision as dp

class import_register(osv.Model):
    _name = 'import.register'
    _description = ''

    @api.one
    @api.depends('invoice_lines_tab.inv_subtotal', 'invoice_lines_tab.tax_value')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.inv_subtotal for line in self.invoice_lines_tab)
        self.amount_tax = sum(xy.tax_value for xy in self.invoice_lines_tab)
        self.amount_total = self.amount_untaxed + self.amount_tax

    _columns = {
        'name': fields.char('Import Register', required=True, copy=False),
        'supplier_id':fields.many2one('res.partner', 'Supplier', required=True,),
        'proforma_invoice_no': fields.char('Proforma Invoice No.'),
        'proforma_invoice_date': fields.date('Proforma Invoice Date'),
        'requisition_no': fields.char('Requisition No.'),
        'purchase_order_no': fields.many2one('purchase.order','Purchase Order No.'),
        'insurance_company':fields.many2one('res.partner', 'Insurance Company'),
        'cover_note_no': fields.char('Cover Note No.'),
        'insurance_note_col_date': fields.date('Insurance Note Collection Date'),
        'eta_date': fields.date('ETA Date'),
        'etd_date': fields.date('ETD Date'),
        'doc_ret_date': fields.date('Document Retirement Date'),
        'lc_value': fields.integer('Value'),
        'insurance_policy_collection': fields.selection([('yes', 'Yes'), ('no', 'No')], string='Insurance Policy Collection'),
        'invoice_lines_tab': fields.one2many('invoice.lines.page','name','Invoice Lines'),
        'lc_info': fields.one2many('lc.info.page', 'name', 'LC Information'),
        'state': fields.selection([('pro_inv', 'Proforma Invoice'), ('ins_col_nt', 'Insurance Collection Note'),('lc_n', 'LC'), ('eta_etd', 'ETA & ETD'), ('doc_ret', 'Document Retirement'), ('ins_pol', 'Insurance Policy'),('done_n', 'Done')], 'State'),
        'amount_untaxed': fields.float(string='Subtotal', store=True, readonly=True, compute='_compute_amount', track_visibility='always'),
        'amount_tax': fields.float(string='Total Tax', store=True, readonly=True, compute='_compute_amount'),
        'amount_total': fields.float(string='Total', store=True, readonly=True, compute='_compute_amount'),
        # 'tax_line': fields.one2many('account.invoice.tax', 'invoice_id', string='Tax Lines',
        # readonly=True, states={'draft': [('readonly', False)]}, copy=True),
        # 'tax_line': fields.float(string='Tax Line'),
        'comment': fields.text('Additional Information')
    }

    _defaults ={
        'state': 'pro_inv',
        'name': 'IR ',
        'amount_untaxed': 0.00,
        'amount_tax': 0.00,
        'amount_total': 0.00,
    }

    def forward1(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'ins_col_nt'})

    def forward2(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'lc_n'})

    def forward3(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'eta_etd'})

    def forward4(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'doc_ret'})

    def forward5(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'ins_pol'})

    def forward6(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'done_n'})

class invoice_lines_page(osv.Model):
    _name = 'invoice.lines.page'
    _description = ''

    @api.one
    @api.depends('unit_price', 'inv_taxes', 'quantity')
    def _compute_price(self):
        # price = self.unit_price
        # taxes = self.inv_taxes.compute_all(price, self.quantity, product=self.product_name)
        taxes = (self.inv_taxes/100)
        self.tax_value = (self.unit_price * self.quantity * taxes)
        self.inv_subtotal = self.unit_price * self.quantity

    _columns = {
        'name': fields.many2one('import.register','Invoice Lines Info Section'),
        'product_name': fields.many2one('product.product','Product'),
        'product_desc': fields.char('Description'),
        'sch_date': fields.date('Scheduled Date'),
        'quantity': fields.integer('Quantity'),
        'product_uom': fields.char('Product UOM'),
        'unit_price': fields.float(string='Unit Price', required=True, ),
        'inv_taxes': fields.float(string='Tax (%)'),
        'tax_value': fields.float(string='Tax'),
        # 'inv_taxes': fields.many2many('account.tax', 'account_invoice_line_taxx', 'invoice_line_idd', 'tax_id', string='Taxes', domain=[('parent_id', '=', False)]),
        'inv_subtotal': fields.float(string='Subtotal', readonly=True, compute='_compute_price', store=True),
    }

    _defaults ={
        'unit_price': 0.00,
        'inv_taxes': 0.00,
        'inv_subtotal': 0.00,
    }





class lc_modes(osv.Model):
    _name = 'lc.modes'
    _columns = {
        'name': fields.char('LC Mode Name'),
    }

class lc_payment_modes(osv.Model):
    _name = 'lc.payment.modes'
    _columns = {
        'name': fields.char('LC Payment Mode Name'),
    }

class lc_info_page(osv.Model):
    _name = 'lc.info.page'
    _description = ''
    _columns = {
        'name': fields.many2one('import.register','LC Info Section'),
        'lc_no': fields.char('LC No.'),
        'lc_date': fields.date('LC Date'),
        'lc_exp_date': fields.date('LC Expire Date'),
        'lc_value': fields.integer('LC Value'),
        'lc_issue_bnk': fields.many2one('res.partner.bank', 'LC Issue Bank'),
        'lc_payment_mode': fields.many2one('lc.payment.modes','LC Payment Mode'),
        'lc_mode': fields.many2one('lc.modes', 'LC Modes'),
        'sequence': fields.integer('Sequence'),
    }

class tax_model(osv.Model):
    _inherit = 'account.invoice.tax'
    _name = 'account.invoice.tax'


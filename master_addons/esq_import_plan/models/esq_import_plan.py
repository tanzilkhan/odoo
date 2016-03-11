from psycopg2 import OperationalError
from openerp.osv import osv, fields, orm
from openerp import api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import openerp


class annual_import_plan(osv.Model):
    _name = 'annual.import.plan'
    _description = 'Annual Import plan'
    _rec_name = 'import_plan_date'
    _columns = {
        'import_plan_date': fields.date('Import Plan Date',required=True),
        'import_plan': fields.one2many('import.plan.per.item', 'name', 'Import Plan'),
        'state': fields.selection([('planning', 'Planning'), ('done', 'Done')], 'State'),
    }

    def planning(self, cr, uid, ids, context=None):
        red = self.pool.get('import.plan.per.item')
        for i in self.browse(cr, uid, ids, context=context):
            for j in i.import_plan:
                red.write(cr, uid, j.id, {'state_change': 'done'})
        return self.write(cr, uid, ids, {'state': 'done'})

    _defaults = {
        'state': 'planning'
    }

class import_plan_per_item(osv.Model):
    _name = 'import.plan.per.item'
    _description = 'Import plan per items'

    @api.one
    @api.depends('bp_quantity', 'ac_quantity', 'bp_value', 'ac_value')
    def _compute_balance_quantity_value(self):
        self.bl_quantity = self.bp_quantity - self.ac_quantity
        self.bl_value = self.bp_value - self.ac_value

    _columns = {
        'name': fields.many2one('annual.import.plan'),
        'product_name': fields.many2one('product.product', 'Items'),
        'product_unit': fields.integer('Units'),
        'bp_quantity': fields.integer('Business Plan Quantity', track_visibility='onchange', state_change={'done':[('readonly',True)]}),
        'bp_value': fields.float('Business Plan Value', track_visibility='onchange', state_change={'done':[('readonly',True)]}),
        'ac_quantity': fields.integer('Actual Import Quantity'),
        'ac_value': fields.float('Actual Import Value'),
        'bl_quantity': fields.integer('Balance Quantity', store=True, readonly=True, compute='_compute_balance_quantity_value'),
        'bl_value': fields.float('Balance Value', store=True, readonly=True, compute='_compute_balance_quantity_value'),
        'state_change': fields.char('Temp')
    }

class procurement_order_addition(osv.Model):
    _inherit = 'procurement.order'

    # @api.model
    # def create(self, values):
    #     return super(procurement_order_addition, self).create(values)

    @api.one
    @api.depends('import_plan_view')
    def _import_plan_view(self):
        plans = self.env['annual.import.plan'].search([('import_plan','=', self.id)])
        self.import_plan_count = len(plans)

    _columns = {
            'state': fields.selection([
            ('cancel', 'Cancelled'),
            ('confirmed', 'Confirmed'),
            ('factory_auth', 'Factory Authorization'),
            ('ho_auth', 'HO Authorization'),
            ('exception', 'Exception'),
            ('procurement', 'Procurement'),
            ('running', 'Running'),
            ('ho_sec_auth', 'HO Authorization'),
            ('done', 'Done')
        ], 'Status', required=True, track_visibility='onchange', copy=False),
            'purchase_type':fields.selection([('local', 'Local'),('order','Order')], 'Purchase Type'),
            'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True, states={'confirmed': [('readonly', False)],'factory_auth': [('readonly', False)],'ho_auth': [('readonly', False)],'ho_sec_auth': [('readonly', False)]}, readonly=True),
            #for smart button
            'import_plan_view': fields.one2many('annual.import.plan', 'import_plan_date', 'Import Plan Date'),
            'import_plan_count': fields.integer(compute='_import_plan_view', string='Import Plans'),
            'factory_gm': fields.char('Test', compute='f_authorize', store=True, readonly=True),
            'senior_gm': fields.char('SG', compute='ho_authorize', store=True, readonly=True),
            'plan_exceed': fields.char('PE', compute='authorize_exceed', store=True, readonly=True),
            'approve_plan': fields.char('AEP', store=True, readonly=True),
            'proc_start': fields.char('PS', store=True, readonly=True),
            'exceed_plan_appr': fields.boolean('Approved Exceed Plan'),
            'proc_order': fields.char('PP', store=True, readonly=True),
    }
    _defaults ={
        'exceed_plan_appr': False,
    }



    def running_pro(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'factory_auth'}, context=context)

    def f_authorize(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'ho_auth', 'factory_gm': 'Approved by Factory'}, context=context)

    def ho_authorize(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'procurement', 'senior_gm':'Approved by Head Office'}, context=context)

    def authorize_exceed(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'procurement', 'plan_exceed': 'Plan exceed procurement request approved', 'exceed_plan_appr': True}, context=context)

    def procure(self, cr, uid, ids, autocommit=False, context=None):
        for procurement_id in ids:
            #we intentionnaly do the browse under the for loop to avoid caching all ids which would be resource greedy
            #and useless as we'll make a refresh later that will invalidate all the cache (and thus the next iteration
            #will fetch all the ids again)
            procurement = self.browse(cr, uid, procurement_id, context=context)
            if procurement.state not in ("running", "done"):
                try:
                    if self._assign(cr, uid, procurement, context=context):
                        res = self._run(cr, uid, procurement, context=context or {})
                        if res:
                            self.write(cr, uid, [procurement.id], {'state': 'running', 'proc_start': 'Procurement has been started'}, context=context)
                            # self.write(cr, uid, [procurement.id], {'state': 'running'}, context=context)
                        else:
                            self.write(cr, uid, [procurement.id], {'state': 'exception'}, context=context)
                    else:
                        self.message_post(cr, uid, [procurement.id], body=_('No rule matching this procurement'), context=context)
                        self.write(cr, uid, [procurement.id], {'state': 'exception'}, context=context)
                    if autocommit:
                        cr.commit()
                except OperationalError:

                    if autocommit:
                        cr.rollback()
                        continue
                    else:
                        raise
        return True

    def ho_sec_authorize(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'ho_sec_auth',  'approve_plan': 'Import Plan Exceeded'}, context=context)

    def excp_pur_order(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'running',  'proc_order': 'No Supplier, PO Created'}, context=context)

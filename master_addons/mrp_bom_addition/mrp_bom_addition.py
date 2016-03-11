# -*- coding: utf-8 -*-
# © 2016 MD Tanzilul Hasan Khan (<http://www.tanzilkhan.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.osv import fields, osv, orm

class temp_item_weight(osv.osv):
    _name = "temp.item.weight"
    _columns = {
        'item_weight': fields.float(),
    }

class bom_modification (osv.Model):
    _inherit = 'mrp.bom'
    _name = 'mrp.bom'

    def onchange_item_weight(self, cr, ids, uid, item_weight):
        cr.execute("DELETE FROM temp_item_weight")
        if item_weight != False:
            cr.execute("INSERT INTO temp_item_weight (item_weight) VALUES ("+str(item_weight)+")")
        return {}

    _columns = {
        'item_weight': fields.float('Item Weight'),
    }

class mrp_bom_percentage(osv.Model):
    _inherit = 'mrp.bom.line'
    _name = 'mrp.bom.line'
    _columns = {
        'weight_percent': fields.float('Percentage Ratio (%)'),
    }

    def percent_calculation(self, cr, uid, ids, weight_percent):
        cr.execute("SELECT item_weight FROM temp_item_weight")
        product_qty = cr.fetchone()
        if product_qty is not None:
            item_weight = product_qty[0]
            weight_percent_actual = weight_percent/100
            product_qty = item_weight * weight_percent_actual
            return {'value':{'product_qty':product_qty}}
        else:
            return {'value':{}}

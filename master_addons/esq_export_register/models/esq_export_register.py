from openerp.osv import osv, fields, orm


class export_register(osv.Model):
    _name = 'export.register'
    _description = ''
    _columns = {
        'up_to_date': fields.date('Date'),
        'register_lines': fields.one2many('export.register.line', 'name', 'Export Register Records'),
        'total_lc_qty': fields.integer('Total L/C Quantity'),
        'total_lc_bl_qty': fields.integer('Total L/C BL Quantity'),
        'all_lst_delivery': fields.date ('All Last Delv. Date'),
        'lc_value': fields.float('L/C Value'),
    }

class lc_tenor(osv.Model):
    _name = 'lc.tenor'
    _description = ''
    _columns = {
        'name': fields.char('L/C Tenor'),
    }

class export_register_line(osv.Model):
    _name = 'export.register.line'
    _description = ''

    def _populate_pi_no(self,cr,uid,context=None):
        sql = "SELECT pi_no,pi_no FROM account_invoice WHERE pi_no IS NOT NULL ORDER BY pi_no"
        cr.execute(sql)
        res = cr.fetchall()
        return res

    def onchange_pi_no(self,cr,uid,ids,pi_no,context=None):
        result = {}
        if pi_no is not False:
            pi_get=self.pool.get('account.invoice')
            id=pi_get.search(cr,uid,[('pi_no','=',pi_no)],context=context)
            if id:
                pi_brw=pi_get.browse(cr,uid,id[0],context=context)
                pi_customer=pi_brw.partner_id.id
                pi_date=pi_brw.date_invoice
                pi_retailer=pi_brw.retailer_name.id

                # pi_product=pi_brw.invoice_line.name
                pi_unit_price=pi_brw.price_unit
                pi_price_subtotatal=pi_brw.price_subtotal
                pi_quantity=pi_brw.quantity
            else:
                pi_customer=False
                pi_unit_price=False
                pi_price_subtotatal=False
                pi_quantity=False
                pi_date=False
                pi_retailer=False

            result['value'] = {'customer': pi_customer,
                               'sales_rate':pi_unit_price,
                               # 'buyer_name':pi_retailer,
                               'sales_value':pi_price_subtotatal,
                               'pi_quant':pi_quantity,
                               'pi_date':pi_date,

                               }

            return result
        else:
            return result

    _columns = {
        'name': fields.char('Name'),
        'sl_no': fields.char('SL. No.'),
        'date': fields.date(''),
        'comm_invoice_no': fields.char('Commercial Invoice No.'),
        'customer': fields.many2one('res.partner', 'Customer', required=True, change_default=True, select=True, track_visibility='always'),
        'pi_no': fields.selection(_populate_pi_no,Type='char',string='Proforma Invoice No.'),
        'pi_date': fields.date('Proforma Invoice Date'),
        'buyer_name': fields.float( 'Buyer Name', required=True),
        'product_ref': fields.many2one('product.product', 'Product Reference'),
        'sales_rate': fields.float('Sales Rate'),
        'sales_value': fields.float('Sales Value'),
        'pi_quant': fields.integer('PI Quantity'),
        'pi_description': fields.char('PI Description'),
        'trans_cost': fields.float('Transportation Cost'),
        'delv_quant': fields.integer('Delivery Quantity'),
        'balance': fields.integer('Balance'),
        'lst_del_date': fields.date('Last Delivery Date'),
        'exp_lc_no': fields.integer('L/C No.'),
        'exp_lc_date': fields.date('L/C Date'),
        'issue_bnk': fields.many2one('res.partner.bank', 'Issuing Bank'),
        'd_sub_party': fields.date('Doc. Submission to Party'),
        'ac_rec_party': fields.date('Acc. Receive from Party'),
        'pi_values': fields.float('PI Values'),
        'nego_bnk': fields.many2one('res.partner.bank', 'Negotiating Bank'),
        'lc_tenor': fields.many2one('lc.tenor', 'L/C Tenor'),
        'ship_dt': fields.date('Shipment Date'),
        'exp_dt': fields.date('Expiry Date'),
        'amend_dt': fields.date('Amendment Date'),
        'ud_no': fields.char('UD No'),
        'ud_rcv_dt': fields.date('UD Receive Date'),
        'status': fields.selection([('advance', 'Advance'), ('tt', 'TT'), ('after_delivery', 'After Delivery')], string='Status'),
        'swift_rcv_dt': fields.date('Swift Receive Date'),
        'lc_transfer_dt': fields.date('L/C Transfer Date'),
        'lc_cp_rcv_dt': fields.date('L/C Copy Receive Date'),
        'delivery_status': fields.integer('Delivery Status'),
        'bl_days': fields.integer('Duration from Submit'),
        'doc_sub_rcv_status': fields.selection([('submit', 'Submit'), ('received', 'Received'), ('false', 'False')], string='Doc. Subm. & Recv. Status'),
        'exp_no': fields.integer('EXP No.'),
        'discrepancy_charge': fields.float('Discrepancy Charges'),
        'duration_adv': fields.integer('Duration for Advance'),
        'lc_rcv_durat': fields.integer('L/C Received Duration from Bank'),
        'ldbc_no': fields.integer('LDBC No.'),
        'bnk_subm_pend': fields.date('Bk Subm. Date & Pend. Party Accp'),
        'coll_pending': fields.integer('Collection Pending'),
        'act_recv_dt': fields.date('Actual Received Date'),
        'mst_lc_no': fields.integer('Master L/C No.'),
        'mst_lc_dt': fields.date('Master L/C Date'),
        'sale_contract_no': fields.integer('Sales Contract No.'),
        'sale_contract_dt': fields.date('Sales Contract Date'),
        'lc_appl_bin': fields.integer('L/C Applicant BIN'),
        'bnk_bin': fields.integer('Bank BIN No'),
        'tin_no': fields.integer('TIN NO.'),
        'irc_no': fields.integer('IRC NO.'),
        'erc_no': fields.integer('ERC NO.'),
        'bond_lcns_no': fields.integer('Bond License NO.'),
        'vat_reg_no': fields.integer('Vat Registration NO.'),
        'hs_code': fields.char('HS Code'),
        'area_code': fields.char('Area Code'),
        'ad_ref_code': fields.char('Ad Reference Code'),
        'bb_circular_no': fields.char('BB Circular No'),
        'exp_perm_no': fields.integer('EXP Permission No.'),
        'exp_perm_dt': fields.date('EXP Permission Date'),
        'others': fields.char('Others'),
        'remarks': fields.text('Remarks'),
    }


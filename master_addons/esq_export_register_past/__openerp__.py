# -*- coding: utf-8 -*-

{
    'name': 'Export Register',
    'version': '1.0',
    'author': 'Tanzil Khan',
    'website': 'https://business-accelerate.com',
    'category': 'Sales',
    'sequence': 1,
    'summary': 'Export register for LC/FDD/LICENSE',
    'depends': ['esq_import_plan', 'sale', 'account','report'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': ['views/esq_export_register_view.xml',
             'report/report_of_export.xml',
             'report/report_of_delivery_challan.xml',
             'report/report_of_packing_list.xml',
             'report/report_of_truck_receipt.xml',
             'report/certificate_of_beneficiary.xml',
             'report/certificate_of_origin.xml',
             ],
}

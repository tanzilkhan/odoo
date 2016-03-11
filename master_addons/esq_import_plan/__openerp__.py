# -*- coding: utf-8 -*-

{
    'name': 'Import Plan and Register',
    'version': '1.0',
    'author': 'Tanzil Khan',
    'website': 'https://business-accelerate.com',
    'category': 'Purchase',
    'sequence': 1,
    'summary': 'Annual Import planning and keeping track in register',
    'depends': ['account','procurement','stock','purchase', 'procurement_jit'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': ['views/esq_import_register_view.xml', 'views/esq_import_plan_view.xml'],
}

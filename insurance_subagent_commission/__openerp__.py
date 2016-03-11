# -*- coding: utf-8 -*-
# © 2016 MD Tanzilul Hasan Khan (<http://www.tanzilkhan.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Subagent for Insurance Business',
    'version': '8.0.1.0',
    'author': 'Tanzil Khan',
    'website': 'http://www.tanzilkhan.com',
    'category': 'Sales',
    'license': 'AGPL-3',
    'sequence': 10,
    'summary': 'Extended for insurance companies',
    'depends': [
        'sale',
        'account',
        'report',
        'hr'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'views/insurance_subagent_commission.xml',
             ],
}

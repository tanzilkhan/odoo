# -*- coding: utf-8 -*-
{
    'name': 'ESQ Payroll Addition',
    'version': '1.0',
    'author': 'Tanzil Khan',
    'category': 'Human Resource',
    'sequence': 1,
    'summary': 'Addition for payroll calculation',
    'depends': ['hr','hr_contract','hr_payroll'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': ['views/esq_payroll_addition_view.xml'],
}
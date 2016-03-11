# -*- coding: utf-8 -*-

{
    'name': 'ESQ_DEV_PAYROLL',
    'version': '1.8',
    'category': 'Others',
    'description': """Custom Payroll Module For ESQ""",
    'author': 'Tanzil Khan',
    'website': 'N/A',
    'license': 'AGPL-3',
    'depends': ['base','hr_payroll','hr', 'hr_contract', 'l10n_in_hr_payroll'],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'active': False,
    'installable': True,
    'application': True,
    'data': [
        'ITV_DEV_PAYROLL_view.xml',
        'work_location.xml'

    ],
}


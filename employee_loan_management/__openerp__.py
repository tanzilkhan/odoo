# -*- coding: utf-8 -*-
# © 2016 MD Tanzilul Hasan Khan (<http://www.tanzilkhan.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
	'name' : 'Employee Loan Management',
	'version' : '8.0.1.0',
	'author' : 'Asma Aly and modified by Tanzil Khan',
	'category' : 'Human Resources',
	'description' : """
		This module was developed by Asmaa Aly and I modified it in some extent.
		
		It allows to manage loans for employee. With this module employee can request loans and pay them
		via payroll system. It also has loan schedule integrated if the interest is inputted.
	""",

	'depends' : ['hr', 'hr_payroll', 'account'],
	'data': [
		'sequences/hr_loan_sequence.xml',
		'datas/hr_payroll_data.xml',
		'views/hr_loan_view.xml',
		'views/hr_payroll_view.xml',
		#'views/board_hr_loan_statistical_view.xml',
	],

	'installable': True,
	'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

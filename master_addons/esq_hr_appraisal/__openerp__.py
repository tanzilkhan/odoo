# -*- coding: utf-8 -*-
{
    'name': 'Appraisal',
    'version': '1.0',
    'author': 'BABL',
    'website': 'https://business-accelerate.com',
    'category': 'HR',
    'sequence': 1,
    'summary': 'Custom Evaluation form',
    'depends': ['hr'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': ['views/esq_hr_appraisal_view.xml'],
    'description': """
Periodical Employees evaluation and appraisals
==============================================

By using this application you can maintain the motivational process by doing periodical evaluations of your employees' performance. The regular assessment of human resources can benefit your people as well your organization.

An evaluation plan can be assigned to each employee. These plans define the frequency and the way you manage your periodic personal evaluations. You will be able to define steps and attach interview forms to each step.

Manages several types of evaluations: bottom-up, top-down, self-evaluations and the final evaluation by the manager.

Key Features
------------
* Ability to create employees evaluations.
* An evaluation can be created by an employee for subordinates, juniors as well as his manager.
* The evaluation is done according to a plan in which various surveys can be created. Each survey can be answered by a particular level in the employees hierarchy. The final review and evaluation is done by the manager.
* Every evaluation filled by employees can be viewed in a PDF form.
* Interview Requests are generated automatically by OpenERP according to employees evaluation plans. Each user receives automatic emails and requests to perform a periodical evaluation of their colleagues.
""",
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Target Gard Module',
    'category': 'Website',
    'summary': 'Target Gard Mobile Application',
    'description': "",
    'depends': ['hr','sale','contacts','account'],
    'data': [
        # 'security/ir.model.access.csv',
            'security/ir.model.access.csv',
            'views/target_guard_view.xml',
            'views/delegates_work_plan.xml',

    ],
    'demo': [
    ],
    'installable': True,
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Target Gard Plans',
    'category': 'Website',
    'summary': 'Target Gard Mobile Application',
    'description': "",
    'depends': ['target_gard','calendar','base'],
    'data': [
        'security/ir.model.access.csv',

        'data/plans_management_config_data.xml',

        'wizard/subplans_generator_view.xml',
        'wizard/saleperson_plans_generator_view.xml',
        
        'views/target_plan_view.xml',
        'views/saleperson_targets_view.xml',
        'views/target_configurations_view.xml',
        'views/plans_management_config.xml',
    ],
    'demo': [
    ],
    'installable': True,
}

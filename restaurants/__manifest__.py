# -*- coding: utf-8 -*-
#########################################################################
#
#    Simple Shop
#    Copyright (C) 2022 Shilal Software Center.
#
##########################################################################
# ________________________________________________________________________

{
    'name': "Restaurants",
    'summary': 'Restaurants System',
    'description': 'This module allows the users to manage their Restaurants',
    'author': "Shilal",
    'company': 'Shilal Software Center (SSC)',
    'website': "https://shilalg.blogspot.com",
    'license': 'OPL-1',
    'price': 100.00,
    'currency': "USD",
    'category': 'Sales',
    'version': '14.0',
    'images': [
        # 'static/description/banner.png'
        ],
    'depends': ['base','sale','board'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_restaurants_view.xml',
        'views/sale_order_view.xml',
        # 'views/error_template_view.xml',
        # 'data/data.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

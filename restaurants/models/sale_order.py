# -*- coding: utf-8 -*-
#########################################################################
#
#    Sale Order
#
##########################################################################
# ________________________________________________________________________

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    restaurant_id = fields.Many2one('res.restaurants', string="Shop")
    

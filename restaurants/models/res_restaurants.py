# -*- coding: utf-8 -*-
#########################################################################
#
#    Restaurants
#
##########################################################################
# ________________________________________________________________________

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ResRestaurants(models.Model):
    _name = "res.restaurants"

    name = fields.Char(string="Name", required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    

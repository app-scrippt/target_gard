# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round


class PlansManagementConfig(models.Model):
    _name = 'plans.management.config'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    manag_type = fields.Selection([
        ('auto','Automatic'),
        ('manual','Manual')],
        required=True,default='manual',string="Management Type")
    next_call = fields.Datetime(string="Next Execution Date")
    interval_number = fields.Integer(string="Execute Every (Hours)")
    state = fields.Selection([
        ('active','Active'),
        ('inactive','Inactive')],
        required=True,default='inactive',string="State")


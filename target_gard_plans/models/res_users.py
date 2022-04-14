# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_


class ResUsers(models.Model):
    _inherit = 'res.users'

    subplan_id = fields.Many2one('target.plan.child', string="SubPlan")

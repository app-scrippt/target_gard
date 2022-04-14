# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_


class TargetPlan(models.Model):
    _inherit = 'calendar.event'

    saleperson_plan_id = fields.Many2one('saleperson.plan', string="saleperson.plan")



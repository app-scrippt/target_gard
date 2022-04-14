# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_
from odoo.exceptions import UserError, ValidationError


class SalepersonCommissionConfig(models.Model):
    _name = 'saleperson.commission.config'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([('draft','Draft'),('active','active'),('archive','Archive')], string='State', default='draft')
    company_id  = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, required=True)
    lines = fields.One2many("saleperson.commission.config.line", "commission_id", string="Lines", required=True)

class SalepersonCommissionConfigLine(models.Model):
    _name = 'saleperson.commission.config.line'

    commission_type = fields.Selection([('fix_amount','Fix Amount'),
        ('sale_percentage','Sales Percentage')], 
        default="fix_amount", required=True, string="Commission Type")
    commission_id = fields.Many2one('saleperson.commission.config')
    commission_due_amount = fields.Float(string="Commission due amount")
    commission_amount = fields.Float(string="Commission amount")

    @api.onchange('commission_amount')
    def _onchange_commission_amount(self):
        if self.commission_type == 'sale_percentage':
            if self.commission_amount > 100:
                raise ValidationError(_("percentage can not be greater than 100 !"))
            if self.commission_amount < 0:
                raise ValidationError(_("percentage can not be less than 0 !"))
        

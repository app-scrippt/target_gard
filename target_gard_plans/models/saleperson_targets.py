# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_


class SalepersonTargetPlan(models.Model):
    _name = 'saleperson.target.plan'

    sub_plan_id = fields.Many2one('target.plan.child', string="Sub Plan", required=True)
    saleperson_id = fields.Many2one('res.users', string="Saleperson", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    target_type = fields.Selection([('amount','Sales By Amount'),
        ('products_qty','Sales By Producs Qty'),
        ('products_amount','Sales By Producs Amount')], string='Target Type', default='amount', required=True)
    lines = fields.One2many('saleperson.target.plan.line', 'plan_id', string="Lines")
    target_amount = fields.Float(string='Target Amount')
    target_achievement_rate = fields.Float(string='Target Achievement Rate', default=0.0)
    commission_id = fields.Many2one('saleperson.commission.config', string="Commission")
    state = fields.Selection([('draft','Draft'),('running','Running'),('done','Done')], string='State', default='draft')


class SalepersonTargetPlanLine(models.Model):
    _name = 'saleperson.target.plan.line'

    plan_id = fields.Many2one('saleperson.target.plan', string="Plan")
    product_id = fields.Many2one('product.template', string="Product", required=True)
    target_amount = fields.Float(string="Target Amount")
    target_qty = fields.Float(string="Target Quantity")


# class SalepersonVisit(models.Model):
#     _name = 'saleperson.visit'

#     saleperson_id = fields.Many2one('res.users', string="Saleperson", required=True, default=lambda self: self.env.user)
#     partner_id = fields.Many2one('res.partner', string="Customer", required=True)
#     saleperson_plan_id = fields.Many2one('saleperson.plan', string="saleperson.plan", required=True)
#     date = fields.Date(string="Date", required=True, default=fields.Date.today())
#     state = fields.Selection([('draft','Draft'),('planed','Planed'),('done','Done')], string='State', default='draft', readonly=True)


class SalepersonPlan(models.Model):
    _name = 'saleperson.plan'

    saleperson_id = fields.Many2one('res.users', string="Saleperson", required=True, default=lambda self: self.env.user)
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today())
    end_date = fields.Date(string="End Date", required=True)
    state = fields.Selection([('draft','Draft'),('planed','Planed'),('done','Done')], string='State', default='draft')
    visit_ids = fields.One2many('calendar.event', 'saleperson_plan_id', string="Visits", required=True)



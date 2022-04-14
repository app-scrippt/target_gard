# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round


class TargetPlan(models.Model):
    _name = 'target.plan'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    company_id  = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    target_type = fields.Selection([('amount','Sales By Amount'),
        ('products_qty','Sales By Producs Qty'),
        ('products_amount','Sales By Producs Amount')], string='Target Type', default='amount', required=True)
    create_subplans_machinism = fields.Selection([('auto','Automatic'),
        ('manual','Manual')], string='Create SubPlans Machinsim',default='auto')
    lines = fields.One2many('target.plan.line', 'plan_id', string="Lines")
    sub_plans = fields.One2many('target.plan.child', 'plan_id', string="Sub Plans")
    state = fields.Selection([('draft','Draft'),('running','Running'),('done','Closed')], string='State', default='draft')
    target_amount = fields.Float(string='Target Amount', compute='calculate_target_amount', readonly=False)
    amount = fields.Float(string='Target Amount')
    target_achievement_rate = fields.Float(string='Target Achievement Rate', default=0.0, readonly=True, compute="calculate_target_achievement_rate")
    maximum_rate = fields.Integer(string='Maximum Rate', default=100)


    @api.onchange('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount and rec.amount <= 0:
                raise ValidationError(_('Target Amount Must Be Greater Than Zero ! '))

    @api.onchange('lines')
    def calculate_target_amount(self):
        target_amount = 0.0
        if self.target_type == 'amount':
            target_amount = self.amount
        else:
            for line in self.lines:
                if self.target_type == 'products_qty':
                    target_amount += line.product_id.list_price*line.target_amount
                if self.target_type == 'products_amount':
                    target_amount += line.target_amount

        self.write({'target_amount':target_amount})


    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_('You cannot delete running or closed plan ! '))
        return super(TargetPlan, self).unlink()


    @api.onchange('start_date','end_date')
    def _check_plan_dates(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError(_("Start Date for the plan cann't be after the end date or same ! "))        


    def confirm_action(self):
        self.state = 'running'


    def done_action(self):
        if self.check_sbuplans_states() == False:
            raise ValidationError(_("You cann't plan before closing it's subplans ! "))
        # self.state = 'done'

    def check_sbuplans_states(self):
        subplans_ids = self.env['target.plan.child'].search([('plan_id','=',self.id),('state','!=','done')])
        if subplans_ids:
            return False
        else:
            return True


    def calculate_target_achievement_rate(self):
        for record in self:
            record.target_achievement_rate = 40

    def genrate_subplans_view(self):
        ctx = {
            'default_plan_id': self.id,
            }
        view_id = self.env.ref('target_gard_plans.subplans_generator_form_view').id
        return {
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'subplans.generator',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'name': _('SubPlans Generator'),
                'target': 'new',
                'context': ctx
            }


class TargetPlanLine(models.Model):
    _name = 'target.plan.line'

    plan_id = fields.Many2one('target.plan', string="Plan")
    child_plan_id = fields.Many2one('target.plan.child', string="Child Plan")
    product_id = fields.Many2one('product.template', string="Product", required=True)
    target_amount = fields.Float(string="Target Amount / Quantity")
    # target_type = fields.Selection([('amount','Sales By Amount'),
    #     ('products_qty','Sales By Producs Qty'),
    #     ('products_amount','Sales By Producs Amount')], string='Target Type', default='products_qty',related='plan_id.target_type')


    # def set_target_type(self):
    #     for record in self:
    #         if record.plan_id:
    #             record.target_type = record.plan_id.target_type
    #         else:
    #             record.target_type = record.child_plan_id.target_type


class TargetPlanChild(models.Model):
    _name = 'target.plan.child'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    plan_id = fields.Many2one('target.plan', string="Parent Plan", domain=[('state','!=','done'),('create_subplans_machinism','=','manual')])
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    child_plan_type = fields.Selection([('amount','Sales By Amount'),
        ('products_qty','Sales By Producs Qty'),
        ('products_amount','Sales By Producs Amount')], 
        string='Sub Plan Type', default='amount', required=True)
    target_amount = fields.Float(string="Target Amount")
    lines = fields.One2many('target.plan.line', 'child_plan_id', string="Lines")
    state = fields.Selection([('draft','Draft'),('running','Running'),('done','Done')], string='State', default='draft')
    target_achievement_rate = fields.Float(string='Target Achievement Rate', readonly=True, compute='calculate_target_achievement_rate')
    target_amount_achievement = fields.Float(string='Target Amount Achievement', readonly=True)
    saleperson_ids = fields.One2many('res.users', 'subplan_id', string="Related Sale Persons")
    saleperson_plans_ids = fields.One2many('saleperson.target.plan', 'sub_plan_id', string="Saleperson Plans")
    create_SP_plans_machinism = fields.Selection([('auto','Automatic'),
        ('manual','Manual')], string='Create S.P Plans Machinsim',default='auto')


    def generate_saleperson_plans(self):
        saleperson_target_amount = self.calculate_saleperson_target_amount()
        ctx = {
            'default_subplan_id': self.id,
            'default_saleperson_target_amount':saleperson_target_amount
            }
        view_id = self.env.ref('target_gard_plans.saleperson_plans_generator_form_view').id
        return {
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'saleperson.plans.generator',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'name': _('Saleperson Plans Generator'),
                'target': 'new',
                'context': ctx
            }


    def calculate_saleperson_target_amount(self):
        saleperson_target_amount = 0.0
        salepersons_number = self.env['res.users'].search_count([('id','in',self.saleperson_ids.ids)])

        if salepersons_number > 0 :
            saleperson_target_amount = self.target_amount/salepersons_number
        return saleperson_target_amount


    def calculate_target_achievement_rate(self):
        for rec in self:
            target_achievement_rate = 0.0
            if rec.target_amount_achievement != 0:
                target_achievement_rate = rec.target_amount_achievement/rec.target_amount*100
            else:
                target_achievement_rate = 0.0
            rec.target_achievement_rate = target_achievement_rate

    def confirm_action(self):
        self.state = 'running'

    @api.onchange('start_date','end_date')
    def validate_plan_dates(self):
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError(_("Start Date for the plan cann't be after the end date or same ! "))

    @api.onchange('start_date','end_date')
    def check_plan_date_rang(self):
        check_value = 0
        subplan_ids = self.env['target.plan.child'].search([('plan_id','=',self.plan_id.id)])
        for subplan in subplan_ids:
            if self.start_date and subplan.start_date and self.end_date and  subplan.end_date:
                if self.start_date >= subplan.start_date and self.start_date <= subplan.end_date:
                    check_value += 1
                if self.end_date >= subplan.start_date and self.end_date <= subplan.end_date:
                    check_value += 1
        if check_value != 0:
            raise ValidationError(_("Start Date for the plan cann't be after the end date or same ! "))


    @api.model
    def create(self,vals):
        self.check_plan_date_rang()
        return super(TargetPlanChild, self).create(vals)



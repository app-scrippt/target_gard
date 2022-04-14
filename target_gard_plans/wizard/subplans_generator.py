# -*- coding: utf-8 -*-
##############################################################################
#
#    
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class SubplansGenerator(models.TransientModel):
    _name = 'subplans.generator'

    plan_id = fields.Many2one('target.plan', string="Plan", required=True)
    duration_type = fields.Selection([('week','Week'),
        ('month','Month'),
        ('3_months','3 Months'),
        ('6_months','6 Months'),
        ('other','Other')], string="SubPlan Duration", required=True)
    duration = fields.Integer(string="Duration by days")

    def generate_subplans(self):
        duration = 0
        if self.duration_type == 'week':
            duration = 7
        if self.duration_type == 'month':
            duration = 30
        if self.duration_type == '3_months':
            duration = 90
        if self.duration_type == '6_months':
            duration = 180
        if self.duration_type == 'other':
            duration = self.duration

        self.create_plans(duration)

    def create_plans(self,duration):
        parent_plan_days = self.calculate_parent_plan_days(self.plan_id.start_date,self.plan_id.end_date)
        subplans_number = int((parent_plan_days/duration))
        target_amount = self.plan_id.target_amount/subplans_number
        start_date = self.plan_id.start_date
        end_date = start_date+relativedelta(days=duration-1)
        for index in range(0,subplans_number):
            if start_date < self.plan_id.end_date:
                self.env['target.plan.child'].create({
                    'name':self.plan_id.name+(_(" / S.P. "))+str(index),
                    'plan_id':self.plan_id.id,
                    'start_date':start_date,
                    'end_date':end_date,
                    'child_plan_type':self.plan_id.target_type,
                    'state':'draft',
                    'target_amount':target_amount
                    })
                start_date = start_date+relativedelta(days=duration)
                end_date = end_date+relativedelta(days=duration)
                if index > subplans_number-4:
                    if self.calculate_parent_plan_days(end_date,self.plan_id.end_date) < duration:
                        end_date = self.plan_id.end_date

    def calculate_parent_plan_days(self,start_date,end_date):
        diff_date = end_date - start_date
        float_plan_days = diff_date.days + float(diff_date.seconds) / 86400
        int_plan_days = int(float_plan_days)

        return int_plan_days



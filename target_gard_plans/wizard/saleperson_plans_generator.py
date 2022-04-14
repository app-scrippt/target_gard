# -*- coding: utf-8 -*-
##############################################################################
#
#    
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class SalePersonPlansGenerator(models.TransientModel):
    _name = 'saleperson.plans.generator'

    subplan_id = fields.Many2one('target.plan.child', string="SubPlan", required=True)
    saleperson_target_amount = fields.Float(string="Saleperson Target Amount")

    def generate_plans(self):
        for user in self.subplan_id.saleperson_ids:
            self.env['saleperson.target.plan'].create({
                'sub_plan_id':self.subplan_id.id,
                'saleperson_id':user.id,
                'start_date':self.subplan_id.start_date,
                'end_date':self.subplan_id.end_date,
                'target_type':self.subplan_id.child_plan_type,
                'target_amount':self.saleperson_target_amount,
                'state':'draft',
            })


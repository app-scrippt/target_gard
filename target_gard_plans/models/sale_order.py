# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        subplan_id = self.get_current_runing_subplan(self.date_order)
        self.apply_on_target_achievement_rate(subplan_id,'confirm')
        return super(SaleOrder, self).action_confirm()

    def action_cancel(self):
        subplan_id = self.get_current_runing_subplan(self.date_order)
        self.apply_on_target_achievement_rate(subplan_id,'cancel')
        return super(SaleOrder, self).action_cancel()

    def apply_on_target_achievement_rate(self,subplan_id,opreation):
        if opreation == 'confirm':
            target_amount_achievement = subplan_id.target_amount_achievement+self.amount_total
        if opreation == 'cancel':
            target_amount_achievement = subplan_id.target_amount_achievement-self.amount_total
        subplan_id.write({
            'target_amount_achievement':target_amount_achievement
            })


    def get_current_runing_subplan(self,date):
        subplan_id = self.env['target.plan.child'].search([('state','=','running'),('start_date','<=',date),('end_date','>=',date)])
        return subplan_id



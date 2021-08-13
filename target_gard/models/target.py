from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class TargetGuardLine(models.Model):
    _name = 'target.line'
    _rec_name = "employee_id"

    target_line_id = fields.Many2one(
        'target.guard', string='sales person')

    employee_id = fields.Many2one(
        'hr.employee',
        string='supervisor',
        required=True,
    )
    
    sales_person_targets = fields.Many2one(
        'hr.employee',
        string='seals person',
        required=True,
    )
    
    

    commission_type = fields.Float(string='commission Type', required=True, digits=0)

    target_amount = fields.Float(string='Target amount', required=True, digits=0)

    commission_amount = fields.Float(
        string='commission amount', required=True, digits=0)

    commission_value = fields.Selection(
        string='Commission',
        default='present',
        selection=[('present', 'Present'), ('amount', 'Amount')]
    )
    
    target_type = fields.Selection(
        string='type',
        default='visit',
        selection=[('visit', 'Visit'), ('sales', 'Sales')]
    )
    
    from_date = fields.Date(
        string='From Date',
        required=True,

    )

    to_date = fields.Date(
        string='To Date',
        required=True,
    )


class TargetGuard(models.Model):
    _name = 'target.guard'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Responsible Admin',
        required=True,

    )

    target_line = fields.One2many(
        'target.line', 'target_line_id', string="Target")

    name = fields.Char(
        string='Name',
        size=64,
        required=True,
    )

    from_date = fields.Date(
        string='From Date',
        required=True,

    )

    to_date = fields.Date(
        string='To Date',
        required=True,
    )

    def open_customer_order(self):
        return {
            'name': _('Sales'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'domain': []

        }

    def open_sales_order(self):
        return {
            'name': _('Sales Order'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('user_id', '=', 'employee_id.user_id')],
        }

    def open_target_order(self):
        return

    @api.constrains('to_date')
    def to_date_check(self):
        if self.from_date:
            if (self.from_date > self.to_date):
                return {
                    'warning': {
                        'title': _('Requested date is too soon.'),
                        'message': _("The delivery date is sooner than the expected date."
                                     "You may be unable to honor the delivery date.")
                    }
                }

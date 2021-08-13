from datetime import datetime, timedelta
from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class DelegateWork(models.Model):
    _name = 'target.delegate'

    geographical_area = fields.Many2many('res.country', string="Address")

    prodect_ids = fields.Many2many('product.product', string=" prodect")
    city_ids = fields.Many2many('res.partner', string="Cities")

    employee_id = fields.Many2one('hr.employee', string="Sales person")

    place = fields.Selection(
        string='Target places',
        default='sales',
        selection=[('alryad', 'Alryad'), ('bury', 'Bury'),
                   ('khartoum', 'Khartoum'), ('bury', 'Bury')]
    )

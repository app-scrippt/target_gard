# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api ,models, fields,_


class ResPartner(models.Model):
    _inherit = 'res.partner'

    lan = fields.Float(
        string='Lan',
    )

    lat = fields.Float(
        string='Lat',
    )


# class ResCompany(models.Model):
#     _inherit = 'res.company'

#     fcm_project_token = fields.Char('FCM Token')


from datetime import datetime
from odoo import models, fields, api


class ResUsers(models.Model):
	_inherit = 'res.users'

	auth2_access_token = fields.Char()
	# verfication_code = fields.Char()
	# code_validity = fields.Datetime('Code Validity')
	device_token = fields.Char()

	# def code_is_expired(self):
	#     self.ensure_one()
	#     return datetime.now() > self.code_validity

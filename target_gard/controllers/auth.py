# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo
from odoo import http, _
from odoo.http import request
from odoo.http import Response
import json
import math, random
import string


class authentication(http.Controller):

	def access_token(self,user_id):
		access_token  = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(700)])
		token_vals = {
					'auth2_access_token' : access_token,

				}
		user_id.sudo().write(token_vals)
		return access_token


	def get_employee_data(self,employee_id,type):
		
		img_url = self.get_employee_image(employee_id.id)
		
		if type == 'all':
			data = {
				'id':employee_id.id,
				'name':employee_id.name,
				'department':employee_id.department_id.name if employee_id.department_id.name else '',
				'nationality':employee_id.country_id.name if employee_id.country_id.name else '',
				'mobile':employee_id.phone if employee_id.phone else '',
				'birthday':str(employee_id.birthday) if employee_id.birthday else '',
				'martial_status':{'id':employee_id.marital if employee_id.marital else '' , 'name':dict(employee_id._fields['marital'].selection).get(employee_id.marital) if employee_id.marital else ''},
				'email':employee_id.private_email if employee_id.private_email else '',
				'address':{'lan':employee_id.address_home_id.lan if employee_id.address_home_id.lan else 0,'lat':employee_id.address_home_id.lat if employee_id.address_home_id.lat else 0, 'address':employee_id.address_home_id.street if employee_id.address_home_id.street else ''},
				'work_address':employee_id.address_id.name if employee_id.address_id.name else '',
				'job':employee_id.job_id.name if employee_id.job_id.name else '',
				'img_url':img_url if img_url else '/',

				# must adding after end customize

				# 'progress':
				# 'current_commission_amount':
				# 'representative_points':
				   }
		else:
			data = {
				'id':employee_id.id,
				'name':employee_id.name,
				'department':employee_id.department_id.name if employee_id.department_id.name else '',
				'job':employee_id.job_id.name if employee_id.job_id.name else '',
				'mobile':employee_id.phone if employee_id.phone else '',
				'img_url':img_url,
					}
		return data


	def authenticate(self):
		"""This method is based on auth2 authentication.
			It will authenticate the users token.
			params :
			Authorization: Authorization should be part of request header
			and it must include Bearer
			Return: It will raise error if token is invalid.

			To use this method import it in your controler 
			from odoo.addons.odoo_auth2.controllers.auth2_authentication import authenticate
			add authentication() in your controller: 

		"""
		error ={}
		headers = dict(list(request.httprequest.headers.items()))
		authHeader = headers['Authorization']
		if authHeader.startswith("Bearer "):
			try:
				access_token = authHeader[7:]
				request.env.cr.execute(
				    "SELECT id  FROM res_users WHERE  auth2_access_token=%s",
				    [access_token]
				)
				data = request.env.cr.fetchone()#request.env['res.users'].search([('auth2_access_token','=',str(access_token))])
				user_id = request.env['res.users'].sudo().browse([data][0])
				if not user_id:
				    raise UserError("Access Token Invalid.")
				user = user_id
				db = request.session.db
				#password = str([data][0][1]).decode('utf-8')
				#request.session.authenticate(db, user.sudo().login , '')
				return request.env['ir.http'].session_info(),user_id
			except Exception as e:
				raise e
		else:
			raise UserError("Access Token Invalid Start with Bearer")

	def get_employee_image(self,employee_id):
		if employee_id:
			request.env.cr.execute(
				"SELECT id FROM ir_attachment WHERE res_model='hr.employee' and res_id=%s",
				[employee_id]
			)
			if request.env.cr.fetchone():
				[attachment_id] = request.env.cr.fetchone()
				img_url = 'http://'+request.httprequest.__dict__['environ']['HTTP_HOST']+'/web/image?model=hr.employee&id=%s&field=image_1920' % employee_id,
				return img_url[0]
			else:
				return '/'
		else:
			return '/'


	@http.route('/target_gard/app_login',auth='public',csrf=False)
	def user_login(self, redirect=None, **post):
		headers={'content-type':'application/json'} 
		data = {} 
		employee_data = []
		access_token = ''
		message = ''
		status = True
		code = 0
		email = post.get('email')
		password = post.get('password')
		fcm_token = post.get('fcm_token')
		lang = post.get('lang')
		users = request.env['res.users']
		user_id = users.sudo().search([('login','=',str(email.strip()))],limit=1)
		try:
			request.params['login_success'] = False
			if request.httprequest.method == 'GET' and redirect and request.session.uid:
				return http.redirect_with_hash(redirect)

			if not request.uid:
				request.uid = odoo.SUPERUSER_ID

			values = request.params.copy()
			try:
				values['databases'] = http.db_list()
			except odoo.exceptions.AccessDenied:
				values['databases'] = None

			if request.httprequest.method == 'POST':
				old_uid = request.uid
				try:
					uid = request.session.authenticate(request.session.db, email, password)
					request.params['login_success'] = True
				except odoo.exceptions.AccessDenied as e:
					request.uid = old_uid
					if e.args == odoo.exceptions.AccessDenied().args:
						values['error'] = _("Wrong login/password")
					else:
						values['error'] = e.args[0]
			else:
				if 'error' in request.params and request.params.get('error') == 'access':
					values['error'] = _('Only employees can access this database. Please contact the administrator.')

			if 'login' not in values and request.session.get('auth_login'):
				values['login'] = request.session.get('auth_login')

			if not odoo.tools.config['list_db']:
				values['disable_database_manager'] = True

			response = request.render('web.login', values)
			response.headers['X-Frame-Options'] = 'DENY'
			if user_id:
				request.env.cr.execute(
					"SELECT COALESCE(password, '') FROM res_users WHERE id=%s",
					[user_id.id]
				)
				[hashed] = request.env.cr.fetchone()
				valid, replacement = users._crypt_context()\
					.verify_and_update(password.strip(), hashed)
				if valid:
					user = user_id
					db = request.session.db
					user_id.write({
						'device_token':fcm_token,
						})
					if lang:
						value = 'en_US'
						if lang == 'en':
							value = 'en_US'
						elif lang == 'ar':
							value = 'ar_001'

						user_id.write({
						'lang':value
						})
					hr_employee = request.env['hr.employee']
					employee_id = hr_employee.search([('user_id','=',user_id.id)],limit=1)
					if employee_id:
						data = self.get_employee_data(employee_id,'all')
						user_lang = 'en'
						lang_name = 'English'
						if user_id.lang == 'en_US':
							user_lang = 'en'
							lang_name = 'English'
						elif lang == 'ar_001':
							user_lang = 'ar'
							lang_name = 'Arabic'
						data['lang'] = {'id':user_lang,'name':lang_name}#dict(request.env['res.users'].fields_get(allfields=['lang'])['lang']['selection'])[user_id.lang]}

					if user_id.auth2_access_token:
						access_token = user_id.auth2_access_token
					else:
						access_token = self.access_token(user_id)

					user_ids = request.env['res.users'].sudo().search([('device_token','=',fcm_token)])
					if user_ids:
						for user in user_ids:
							user.write({
							'device_token':'',
							})

					message = 'Success'
					status = True
					code = 200
				else:
					message = 'Wrong login/password'
					status = False
					code = 400
			else:
				message = 'Wrong login/password'
				status = False
				code = 400
		

			vals = {
				'data' : {'access_token':access_token,'user_data':data},
				'status':status,
				'message':message,
				'error_code':code
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'data':{},'status':False,'message': e.__str__() ,'error_code':500}),headers=headers)


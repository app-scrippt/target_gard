
import json
import base64
from odoo import http, _
from odoo.http import request
from odoo.http import Response
from odoo import api , fields, models,_

class TargetGard(http.Controller):

	def authenticate(self):
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
				data = request.env.cr.fetchone()
				user_id = request.env['res.users'].sudo().browse([data][0])
				if not user_id:
				    raise UserError("Access Token Invalid.")
				user = user_id
				db = request.session.db
				#request.session.authenticate(db, user.sudo().login , '222')
				return request.env['ir.http'].session_info(),user_id
			except Exception as e:
			    raise e
		else:
			raise UserError("Access Token Invalid Start with Bearer")

	def get_customer_image(self,partner_id):
		if partner_id:
			request.env.cr.execute(
				"SELECT id FROM ir_attachment WHERE res_model='res.partner' and res_id=%s",
				[partner_id]
			)
			if request.env.cr.fetchone():
				img_url = 'http://'+request.httprequest.__dict__['environ']['HTTP_HOST']+'/web/partner_image/%s/image_1920/res.partner' % partner_id,
				return img_url[0]
			else:
				return '/'
		else:
			return '/'

	def get_customer_data(self,partner_id):
		tags = []
		img_url = self.get_customer_image(partner_id.id)
		for category in partner_id.category_id:
				tag = {
				'id':category.id,
				'name':category.name,
				}
				tags.append(tag)
		customer_data = {
			'id':partner_id.id,
			'type':{'id':partner_id.company_type if partner_id.company_type else '' , 'name':dict(partner_id._fields['company_type'].selection).get(partner_id.company_type) if partner_id.company_type else ''},
			'name':partner_id.name,
			'email':partner_id.email if partner_id.email else '',
			'phone':partner_id.phone if partner_id.phone else '',
			'mobile':partner_id.mobile if partner_id.mobile else '',
			'tags':tags,
			'job':partner_id.function if partner_id.function else '',
			'address':{
			'type':{'id':partner_id.type if partner_id.type else '' , 'name':dict(partner_id._fields['type'].selection).get(partner_id.type) if partner_id.type else ''},
			'country':{'id':partner_id.country_id.id , 'name':partner_id.country_id.name} if partner_id.country_id.name else '',
			'city':partner_id.city if partner_id.city else '',
			'state':{'id':partner_id.state_id.id , 'name':partner_id.state_id.name}  if partner_id.state_id.name else '',
			'street':partner_id.street if partner_id.street else '',
			},
			'note':partner_id.comment if partner_id.comment else '',
			'sale_persone':partner_id.user_id.name if partner_id.user_id.name else '',
			'img_url':img_url,
			}
		return customer_data

	@http.route('/get_customers', type='http', auth='public', methods=['GET'], csrf=False)
	def _get_customers(self , **post):
		headers={'content-type':'application/json'} 
		try:
			#self.authenticate()
			customers = []
			customer_data = dict() 
			res_partner = request.env['res.partner']
			res_partner_ids = res_partner.sudo().search([('customer_rank','=',1)],order='id desc')
			for partner_id in res_partner_ids:
				img_url = self.get_customer_image(partner_id.id)
				customer_data = {
					'id':partner_id.id,
					'name':partner_id.name,
					'mobile':partner_id.phone if partner_id.phone else '',
					'img_url':img_url,
					}
				customers.append(customer_data)

			values = {
				'data' : {'title':'all' , 'customers':customers},
				'status':True,
				'message':'Success',
				'error_code':'200'
			}

			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/get_customer_details', type='http', auth='public', methods=['GET'], csrf=False)
	def get_customer_details(self , **post):
		headers={'content-type':'application/json'} 
		try:
			#self.authenticate()
			customer_id = post.get('customer_id')
			res_partner = request.env['res.partner']
			partner_id = res_partner.sudo().search([('id','=',int(customer_id))],order='id desc')
			
			customer_data = self.get_customer_data(partner_id)

			values = {
				'data' :customer_data ,
				'status':True,
				'message':'Success',
				'error_code':'200'
			}

			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)
	
	@http.route('/update_customer_profile', type='http', auth='public', methods=['POST'], csrf=False)
	def update_customer_profile(self , **post):
		headers={'content-type':'application/json'} 
		status = True
		code = 0
		try:
			#session , user_id = self.authenticate()
			customer_data = dict()
			customer_id = post.get('customer_id')
			name = post.get('name')
			company_type = post.get('company_type')
			email = post.get('email')
			phone = post.get('phone')
			mobile = post.get('mobile')
			note = post.get('note')
			tags = post.get('tags')
			profile_photo = post.get('profile_photo')
			job = post.get('job')
			country = post.get('country')
			city = post.get('city')
			state = post.get('state')
			street = post.get('street')
			sale_person = post.get('sale_person')
			partner_id = request.env['res.partner'].sudo().search([('id','=',int(customer_id))],limit=1)
			if partner_id:
				if name:
					partner_id.sudo().write({
						'name':name.strip()
						})
				if company_type:
					partner_id.sudo().write({
						'company_type':company_type
						})
				if email:
					partner_id.sudo().write({
						'email':email
						})
				if mobile:
					partner_id.sudo().write({
						'mobile':mobile.strip()
						})
				if phone:
					partner_id.sudo().write({
						'phone':phone.strip()
				 		})
				if profile_photo:
					filecontent = base64.b64encode(profile_photo.read())
					partner_id.write({
						'image_1920':filecontent
						})
				if note:
					partner_id.sudo().write({
						'comment':note
						})

				if tags:
					tags_data = list(tags.replace("[", "").replace("]", ""))
					if tags_data:
						tags_data = list(map(int,tags.replace("[", "").replace("]", "").split(',')))
					partner_id.sudo().write({
						'category_id':[(6, 0, tags_data)],
						})
				if job:
					partner_id.sudo().write({
						'function':job
						})
				if sale_person:
					partner_id.sudo().write({
						'sale_person':sale_person
						})
				if country:
					partner_id.sudo().write({
						'country_id':int(country)
						})
				if city:
					partner_id.sudo().write({
						'city':city
						})
				if state:
					partner_id.sudo().write({
						'state_id':int(state)
						})
				if street:
					partner_id.sudo().write({
						'street':street
						})

				customer_data = self.get_customer_data(partner_id)
				status = True
				message = 'Success'
				code = 200
			else:
				status = False
				message = 'No customer'
				code = 400

			vals = {
				'data' : [customer_data],
				'status':status,
				'message':message,
				'error_code':code
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/create_customer', type='http', auth='public', methods=['POST'], csrf=False)
	def create_customer(self , **post):
		headers={'content-type':'application/json'} 
		status = True
		code = 0
		try:
			#session , user_id = self.authenticate()
			employee_id = ''
			name = post.get('name')
			company_type = post.get('company_type')
			email = post.get('email')
			phone = post.get('phone')
			mobile = post.get('mobile')
			note = post.get('note')
			tags = post.get('tags')
			profile_photo = post.get('profile_photo')
			job = post.get('job')
			country = post.get('country')
			city = post.get('city')
			state = post.get('state')
			street = post.get('street')
			sale_person = post.get('sale_person')
			if sale_person:
				employee_id = request.env['hr.employee'].sudo().browse(int(sale_person))
			if tags:
				tags_data = list(tags.replace("[", "").replace("]", ""))
				if tags_data:
					tags_data = list(map(int,tags.replace("[", "").replace("]", "").split(',')))

			if profile_photo:
				filecontent = base64.b64encode(profile_photo.read())
			partner_id = request.env['res.partner'].sudo().create({
				'name':name.strip(),
				'company_type':company_type,
				'email':email,
				'mobile':mobile.strip(),
				'phone':phone.strip(),
				'comment':note,
				'category_id':[(6, 0, tags_data)],
				'function':job,
				'user_id':employee_id.user_id.id,
				'image_1920':filecontent,
				'customer_rank':1,
				'country_id':int(country) if country else '',
				'city':city,
				'state_id':int(state) if state else '',
				'street':street,
				})
			
			customer_data = self.get_customer_data(partner_id)
			status = True
			message = 'Success'
			code = 200
			

			vals = {
				'data' : [customer_data],
				'status':status,
				'message':message,
				'error_code':code
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/get_customer_tags', type='http', auth='public', methods=['GET'], csrf=False)
	def get_customer_tags(self , **post):
		headers={'content-type':'application/json'} 
		try:
			data = []
			#self.authenticate()
			categories = []
			partner_category_ids = request.env['res.partner.category'].sudo().search([],order='id desc')
			for category in partner_category_ids:
				vals = {
				'id':category.id,
				'name':category.name
				}
				categories.append(vals)

			vals = {
			'data':categories,
			'status':True,
			'message':'Success',
			'error_code':200
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/get_customer_types', type='http', auth='public', methods=['GET'], csrf=False)
	def get_customer_types(self , **post):
		headers={'content-type':'application/json'} 
		try:
			data = []
			#self.authenticate()
			res_partner = request.env['res.partner']
			company_type_dict = dict(res_partner._fields['company_type'].selection)
			for cotype in company_type_dict.keys():
				company_type = {
				'id':cotype,
				'name':company_type_dict.get(cotype)
				}
				data.append(company_type)
			vals = {
			'data':data,
			'status':True,
			'message':'Success',
			'error_code':200
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/get_customer_addresses', type='http', auth='public', methods=['GET'], csrf=False)
	def get_customer_addresses(self , **post):
		headers={'content-type':'application/json'} 
		try:
			#self.authenticate()
			addresses = []
			customer_id = post.get('customer_id')
			res_partner = request.env['res.partner']
			partner_id = res_partner.sudo().search([('id','=',int(customer_id))],order='id desc')
			for address in partner_id.child_ids:
				customer_data = {
					'id':address.id,
					'name':address.name,
					'type':{'id':address.type if address.type else '' , 'name':dict(address._fields['type'].selection).get(address.type) if address.type else ''},
					'country':{'id':partner_id.country_id.id , 'name':partner_id.country_id.name} if partner_id.country_id.name else '',
					'city':partner_id.city if partner_id.city else '',
					'state':{'id':partner_id.state_id.id , 'name':partner_id.state_id.name}  if partner_id.state_id.name else '',
					'street':partner_id.street if partner_id.street else '',
					}
				addresses.append(customer_data)

			values = {
				'data' :addresses ,
				'status':True,
				'message':'Success',
				'error_code':'200'
			}

			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)


	@http.route('/update_customer_address', type='http', auth='public', methods=['POST'], csrf=False)
	def update_customer_address(self , **post):
		headers={'content-type':'application/json'} 
		status = True
		code = 0
		try:
			#session , user_id = self.authenticate()
			address_data = dict()
			address_id = post.get('address_id')
			name = post.get('name')
			type = post.get('type')
			email = post.get('email')
			phone = post.get('phone')
			mobile = post.get('mobile')
			note = post.get('note')
			country = post.get('country')
			city = post.get('city')
			state = post.get('state')
			street = post.get('street')
			partner_id = request.env['res.partner'].sudo().search([('id','=',int(address_id))],limit=1)
			if partner_id:
				if name:
					partner_id.sudo().write({
						'name':name.strip()
						})
				if type:
					partner_id.sudo().write({
						'type':type
						})
				if email:
					partner_id.sudo().write({
						'email':email
						})
				if mobile:
					partner_id.sudo().write({
						'mobile':mobile.strip()
						})
				if phone:
					partner_id.sudo().write({
						'phone':phone.strip()
				 		})
				if note:
					partner_id.sudo().write({
						'comment':note
						})
				if country:
					partner_id.sudo().write({
						'country_id':int(country)
						})
				if city:
					partner_id.sudo().write({
						'city':city
						})
				if state:
					partner_id.sudo().write({
						'state_id':int(state)
						})
				if street:
					partner_id.sudo().write({
						'street':street
						})

				address_data = {
					'id':partner_id.id,
					'name':partner_id.name,
					'type':{'id':partner_id.type if partner_id.type else '' , 'name':dict(partner_id._fields['type'].selection).get(partner_id.type) if partner_id.type else ''},
					'country':{'id':partner_id.country_id.id , 'name':partner_id.country_id.name} if partner_id.country_id.name else '',
					'city':partner_id.city if partner_id.city else '',
					'state':{'id':partner_id.state_id.id , 'name':partner_id.state_id.name}  if partner_id.state_id.name else '',
					'street':partner_id.street if partner_id.street else '',
					}
				status = True
				message = 'Success'
				code = 200
			else:
				status = False
				message = 'No customer'
				code = 400

			vals = {
				'data' : [address_data],
				'status':status,
				'message':message,
				'error_code':code
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)


	@http.route('/create_customer_address', type='http', auth='public', methods=['POST'], csrf=False)
	def create_customer_address(self , **post):
		headers={'content-type':'application/json'} 
		status = True
		code = 0
		try:
			#session , user_id = self.authenticate()
			address_id = ''
			customer_id = post.get('customer_id')
			name = post.get('name')
			type = post.get('type')
			email = post.get('email')
			phone = post.get('phone')
			mobile = post.get('mobile')
			note = post.get('note')
			country = post.get('country')
			city = post.get('city')
			state = post.get('state')
			street = post.get('street')
			if customer_id:
				partner_id = request.env['res.partner'].sudo().search([('id','=',int(customer_id))])
				if partner_id:
					address_id = request.env['res.partner'].sudo().create({
						'parent_id':partner_id.id,
						'name':name.strip(),
						'type':type,
						'email':email,
						'mobile':mobile.strip(),
						'phone':phone.strip(),
						'comment':note,
						'country_id':int(country) if country else '',
						'city':city,
						'state_id':int(state) if state else '',
						'street':street,
						})
					if address_id:
				
						address_data = {
							'id':address_id.id,
							'name':partner_id.name,
							'type':{'id':partner_id.type if partner_id.type else '' , 'name':dict(partner_id._fields['type'].selection).get(partner_id.type) if partner_id.type else ''},
							'country':{'id':partner_id.country_id.id , 'name':partner_id.country_id.name} if partner_id.country_id.name else '',
							'city':partner_id.city if partner_id.city else '',
							'state':{'id':partner_id.state_id.id , 'name':partner_id.state_id.name}  if partner_id.state_id.name else '',
							'street':partner_id.street if partner_id.street else '',
							}
					status = True
					message = 'Success'
					code = 200
				else:
					status = False
					message = 'Customer Not Found'
					code = 400

			vals = {
				'data' : [address_data],
				'status':status,
				'message':message,
				'error_code':code
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)


	@http.route('/get_address_types', type='http', auth='public', methods=['GET'], csrf=False)
	def get_address_types(self , **post):
		headers={'content-type':'application/json'} 
		try:
			data = []
			#self.authenticate()
			res_partner = request.env['res.partner']
			address_type_dict = dict(res_partner._fields['type'].selection)
			for addtype in address_type_dict.keys():
				address_type = {
				'id':addtype,
				'name':address_type_dict.get(addtype)
				}
				data.append(address_type)
			vals = {
			'data':data,
			'status':True,
			'message':'Success',
			'error_code':200
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/get_countries', type='http', auth='public', methods=['GET'], csrf=False)
	def get_countries(self , **post):
		headers={'content-type':'application/json'} 
		try:
			
			#self.authenticate()
			data = []
			countries = []
			country_ids = request.env['res.country'].sudo().search([],order='id desc')
			for country in country_ids:
				vals = {
				'id':country.id,
				'name':country.name
				}
				countries.append(vals)

			vals = {
			'data':countries,
			'status':True,
			'message':'Success',
			'error_code':200
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/get_states', type='http', auth='public', methods=['GET'], csrf=False)
	def get_states(self , **post):
		headers={'content-type':'application/json'} 
		try:
			
			#self.authenticate()
			data = []
			states = []
			country_id = post.get('country_id')
			country_state_ids = request.env['res.country.state'].sudo().search([('country_id','=',int(country_id))],order='id desc')
			for country in country_state_ids:
				vals = {
				'id':country.id,
				'name':country.name
				}
				states.append(vals)

			vals = {
			'data':states,
			'status':True,
			'message':'Success',
			'error_code':200
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/get_customer_visits', type='http', auth='public', methods=['GET'], csrf=False)
	def get_customer_visits(self , **post):
		headers={'content-type':'application/json'} 
		try:
			#self.authenticate()
			visits = []
			visit_data = ''
			customer_id = post.get('customer_id')
			mail_activity_ids = request.env['mail.activity'].sudo().search([('res_model','=','res.partner'),('res_id','=',int(customer_id))],order='id desc')
			for activity in mail_activity_ids:
				visit_data = {
					'id':activity.id,
					'discription':activity.summary,
					'type':{'id':activity.activity_type_id.id , 'name':activity.activity_type_id.name} if activity.activity_type_id else '',
					'date':str(activity.date_deadline) ,
					}
				visits.append(visit_data)

			values = {
				'data' :visits ,
				'status':True,
				'message':'Success',
				'error_code':'200'
			}

			return Response(json.dumps(values),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

	@http.route('/update_customer_visit', type='http', auth='public', methods=['POST'], csrf=False)
	def update_customer_visit(self , **post):
		headers={'content-type':'application/json'} 
		status = True
		code = 0
		try:
			#session , user_id = self.authenticate()
			visit_data = dict()
			visit_id = post.get('visit_id')
			discription = post.get('discription')
			date = post.get('date')
			type_id = post.get('type_id')
			
			activity_id = request.env['mail.activity'].sudo().search([('id','=',int(visit_id))],limit=1)
			if activity_id:
				if discription:
					activity_id.sudo().write({
						'summary':discription.strip()
						})
				if type:
					activity_id.sudo().write({
						'activity_type_id':int(type_id)
						})
				if date:
					activity_id.sudo().write({
						'date_deadline':date
						})	

				visit_data = {
					'id':activity_id.id,
					'discription':activity_id.summary,
					'type':{'id':activity_id.activity_type_id.id , 'name':activity_id.activity_type_id.name} if activity_id.activity_type_id else '',
					'date':str(activity_id.date_deadline) ,
					}
				status = True
				message = 'Success'
				code = 200
			else:
				status = False
				message = 'No customer'
				code = 400

			vals = {
				'data' : [visit_data],
				'status':status,
				'message':message,
				'error_code':code
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)


	@http.route('/create_customer_visit', type='http', auth='public', methods=['POST'], csrf=False)
	def create_customer_visit(self , **post):
		headers={'content-type':'application/json'} 
		status = True
		code = 0
		try:
			#session , user_id = self.authenticate()
			visit_data = ''
			customer_id = post.get('customer_id')
			discription = post.get('discription')
			type_id = post.get('type_id')
			date = post.get('date')

			if customer_id:
				partner_id = request.env['res.partner'].sudo().search([('id','=',int(customer_id))])
				if partner_id:
					res_model_id = request.env['ir.model'].sudo().search([('model','=','res.partner')], limit=1)
					activity_id = request.env['mail.activity'].sudo().create({
						'res_id':partner_id.id,
						'res_model_id':res_model_id.id,
						'res_model':'res.partner',
						'summary':discription.strip(),
						'activity_type_id':int(type_id),
						'date_deadline':str(date),
						})
					if activity_id:
						visit_data = {
							'id':activity_id.id,
							'discription':activity_id.summary,
							'type':{'id':activity_id.activity_type_id.id , 'name':activity_id.activity_type_id.name} if activity_id.activity_type_id else '',
							'date':str(activity_id.date_deadline) ,
							#'user_id':user_id.id,
							}
					status = True
					message = 'Success'
					code = 200
				else:
					status = False
					message = 'Customer Not Found'
					code = 400

			vals = {
				'data' : [visit_data],
				'status':status,
				'message':message,
				'error_code':code
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)


	@http.route('/get_visit_types', type='http', auth='public', methods=['GET'], csrf=False)
	def get_visit_types(self , **post):
		headers={'content-type':'application/json'} 
		try:
			
			#self.authenticate()
			types = []
			activity_type_ids = request.env['mail.activity.type'].sudo().search([],order='id desc')
			for activity_type in activity_type_ids:
				vals = {
				'id':activity_type.id,
				'name':activity_type.name
				}
				types.append(vals)

			vals = {
			'data':types,
			'status':True,
			'message':'Success',
			'error_code':200
			}
			return Response(json.dumps(vals),headers=headers)
		except Exception as e:
			return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)

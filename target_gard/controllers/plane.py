import json
import base64
import odoo
from odoo import http, _
from odoo.http import request
from odoo.http import Response
from datetime import date, time, datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import date, time, datetime, timedelta

class PlanController(http.Controller):
    @http.route('/get_sale_person_work_plans',  type='http', methods=['GET'], auth='public', csrf=False)
    def get_targets(self, **post):
        headers={'content-type':'application/json'} 
        try:

            plan_deatails = []
            print(type(post.get('sale_person_id')))
            
            sale_person_id = int(post.get('sale_person_id'))
            print('-------1111111111111-----------------',sale_person_id)
            res_plan = request.env['target.delegate']
            plan_obj_id = res_plan.sudo().search([])
        
            for plan_id in plan_obj_id:
                products = []
                geographical =[]
                city =[]
                for product_id in plan_id.prodect_ids:
                    products.append({'id':product_id.id , 'name':product_id.name})
                for geographical_areas in plan_id.geographical_area:
                    geographical.append({'id':geographical_areas.id , 'name':geographical_areas.name})
                for city_id in plan_id.city_ids:
                    city.append({'id':city_id.id , 'name':city_id.name})
                plan_data ={
                    'sales person':{'id':plan_id.employee_id.id , 'name':plan_id.employee_id.name}  if plan_id.employee_id.name else '',
                    'products': products,
                    'target geographic area':geographical,
                    'city':city,
                    'place':{'id':plan_id.place if plan_id.place else '' , 'name':dict(plan_id._fields['place'].selection).get(plan_id.place) if plan_id.place else ''},
                }
                plan_deatails.append(plan_data)
            values = {
                'data' :plan_deatails ,
                'status':True,
                'message':'Success',
                'error_code':'200'
            }
            return Response(json.dumps(values), headers=headers)
        except Exception as e:
            return Response(json.dumps({'message': e.__str__(), 'error_code': 500, 'status': False, 'data': {}}), headers=headers)
    
    @http.route('/update_work_plan',  type='http', methods=['POST'], auth='public', csrf=False)
    def get_targets(self, **post):
        headers={'content-type':'application/json'} 
        print('-----------------------------plan----------------------------')
        try:  
            
            products = []
            geographical =[]
            city =[]
            sale_person_id = int(post.get('sale_person_id'))
            geographical_area = post.get('geographical_area')
            prodect_ids = post.get('prodect_ids')
            city_ids = post.get('city_ids')
            employee_id = post.get('employee_id')
            place = post.get('place')
            
            plan_obj_id = request.env['target.delegate'].sudo().search([('id', '=', sale_person_id)])
            print('----------------------update target plane--------------',plan_obj_id)
            
            for citys in plan_obj_id.city_ids:
                city.append({'id':citys.id , 'name':citys.name})
            for product in plan_obj_id.prodect_ids:
                products.append({'id':product.id , 'name':product.name})
            for geographic in plan_obj_id.geographical_area:
                geographical.append({'id':geographic.id , 'name':geographic.name})
                
            if plan_obj_id:
                if geographical_area:
                    plan_obj_id.sudo().write({
                        'geographical_area': [(6, 0, geographical)]
                    })
                if prodect_ids:
                    plan_obj_id.sudo().write({
                        'prodect_ids':[(6, 0, products)],
                    })
                if city_ids:
                    plan_obj_id.sudo().write({
                        'city_ids':[(6, 0, city)],
                    })
                if employee_id:
                    plan_obj_id.sudo().write({
                        'employee_id': employee_id
                    })
                if place:
                    plan_obj_id.sudo().write({
                        'place': place
                    })
                plan_data = {
                    'name': {'id':plan_obj_id.employee_id.id , 'name':plan_obj_id.employee_id.name}  if plan_obj_id.employee_id.name else '',
                    'place':{'id':plan_obj_id.place if plan_obj_id.place else '' , 'name':dict(plan_obj_id._fields['place'].selection).get(plan_obj_id.place) if plan_obj_id.place else ''},
                    'city':city,
                    'geographical':geographical,
                    'products':products
                    


                }
            vals = {
                'data': plan_data,
                'status': True,
                'message': 'Success',
                'error_code': 200
            }
            return Response(json.dumps(vals), headers=headers)
        except Exception as e:
            return Response(json.dumps({'message': e.__str__(), 'error_code': 500, 'status': False, 'data': {}}), headers=headers)

                

            
            
            

            
            
            

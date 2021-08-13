import json
import odoo
from odoo import http, _
from odoo.http import request
from odoo.http import Response
from datetime import date, time, datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import date, time, datetime, timedelta


class TargetController(http.Controller):
    @http.route('/get_targets',  type='http', methods=['GET'], auth='public', csrf=False)
    def get_targets(self, **post):
        print('------------------------')
        headers = {'content-type': 'application/json'}
        try:
            target_data = dict()
            target_rec = []
            res_target = request.env['target.guard']
            target = res_target.sudo().search([])
            for targets in target:
                target_data = {
                    'name': targets.name,
                    'date_from': fields.Datetime.to_string(targets.from_date),
                    'date_to': fields.Datetime.to_string(targets.to_date)
                }
                target_rec.append(target_data)
            values = {
                'data': target_rec,
                'status': True,
                'message': 'Success',
                'error_code': '200'
            }
            print('-------777-----------------', values)
            return Response(json.dumps(values), headers=headers)
        except Exception as e:
            print('-------6666-----------------')
            return Response(json.dumps({'message': e.__str__(), 'error_code': 500, 'status': False, 'data': {}}), headers=headers)

    @http.route('/create_target', type='http', auth='public', methods=['POST'], csrf=False)
    def create_target_gard(self, **post):
        headers = {'content-type': 'application/json'}
        status = True
        code = 0
        values = dict()
        try:
            trget_gurd_id = ''
            name = post.get('name')
            employee_id = int(post.get('employee_id'))
            to_date = post.get('to_date')
            from_date = post.get('from_date')

            if employee_id:
                target_id = request.env['target.guard'].sudo().search(
                    [('id', '=', employee_id)], limit=1)
                if target_id:
                    trget_gurd_id = request.env['target.guard'].sudo().create({
                        'name': name.strip(),
                        'employee_id': employee_id,
                        'to_date': to_date,
                        'from_date': from_date
                    })
                    if trget_gurd_id:
                        target_data = {
                            'employee_id': trget_gurd_id.employee_id.id,
                            'name': trget_gurd_id.name,
                            'to_date':  fields.Datetime.to_string(trget_gurd_id.to_date),
                            'from_date':  fields.Datetime.to_string(trget_gurd_id.from_date)

                        }
                        status = True
                        message = 'Success'
                        code = 200
                else:

                    status = False
                    message = 'target not found yet'
                    code = 400

                vals = {
                    'data':  [target_data],
                    'status': status,
                    'message': message,
                    'error_code': code,
                    'status': True,
                }
            return Response(json.dumps(vals), headers=headers)
        except Exception as e:
            return Response(json.dumps({'message': e.__str__(), 'error_code': 500, 'status': False, 'data': {}}), headers=headers)

    @http.route('/update_target', type='http', auth='public', methods=['POST'], csrf=False)
    def update_target(self, **post):
        headers = {'content-type': 'application/json'}
        status = True
        try:
            trget_gurd_id = ''
            name = post.get('name')
            employee_id = int(post.get('employee_id'))
            to_date = post.get('to_date')
            from_date = post.get('from_date')
            target_id = request.env['target.guard'].sudo().search(
                [('id', '=', employee_id)], limit=1)
            if target_id:
                if name:
                    target_id.sudo().write({
                        'name': name.strip()
                    })
                if employee_id:
                    target_id.sudo().write({
                        'employee_id': employee_id
                    })
                if from_date:
                    target_id.sudo().write({
                        'from_date': from_date
                    })
                if to_date:
                    target_id.sudo().write({
                        'to_date': to_date
                    })
                target_data = {
                    'id': target_id.id,
                    'name': target_id.employee_id.name,
                    'from_date': fields.Datetime.to_string(target_id.from_date),
                    'to_date': fields.Datetime.to_string(target_id.to_date)
                }
                status = True
                message = 'Success'
                code = 200
            else:
                status = False
                message = 'No target'
                code = 400

            vals = {
                'data': [target_data],
                'status': status,
                'message': message,
                'error_code': code
            }
            return Response(json.dumps(vals), headers=headers)
        except Exception as e:
            return Response(json.dumps({'message': e.__str__(), 'error_code': 500, 'status': False, 'data': {}}), headers=headers)

    @http.route('/get_target_deatails',  type='http', methods=['GET'], auth='public', csrf=False)
    def get_targets(self, **post):
        print('-------1111111111111000000000000-----------------')
        
        headers={'content-type':'application/json'} 
        try: 
            target_deatails = []
            print('-------1111111111111-555555----------------',post.get('target_id'))
            print(type(post.get('target_id')))
            
            target_id = int(post.get('target_id'))
            print('-------1111111111111-----------------',target_id)

            target_obj_id = request.env['target.guard'].sudo().search([('id','=',target_id)])
            
            
            
            for line in target_obj_id.target_line:
                target_data = {
                    'id':line.id,
                    'name':target_obj_id.name,
                    'date_from': fields.Datetime.to_string(line.from_date),
                    'to_date':  fields.Datetime.to_string(line.to_date),
                    'supervisor':{'id':line.employee_id.id , 'name':line.employee_id.name}  if line.employee_id.name else '',
                    'sales person':{'id':line.employee_id.id , 'name':line.employee_id.name}  if line.employee_id.name else '',
                    'target amount':line.target_amount,
                    'commission_amount': line.commission_amount,
                    'target_type':{'id':line.target_type if line.target_type else '' , 'name':dict(line._fields['type'].selection).get(line.target_type) if line.target_type else ''},
                    
                }
                target_deatails.append(target_data)
            
            values = {
                'data' :target_deatails ,
                'status':True,
                'message':'Success',
                'error_code':'200'
            }
            return Response(json.dumps(values), headers=headers)
        except Exception as e:
            return Response(json.dumps({'message': e.__str__(), 'error_code': 500, 'status': False, 'data': {}}), headers=headers)
        
        
    @http.route('/update_target_deatails', type='http', auth='public', methods=['POST'], csrf=False)
    def update_target(self , **post):
        headers={'content-type':'application/json'} 
        status = True
        message=''
        code = 0
        try:
            
            target_data = dict()
            target_id = int(post.get('target_id'))
            
            name = post.get('name')
            to_date = post.get('to_date')
            from_date = post.get('from_date')
            target_amount = int(post.get('target_amount'))
            commission_type = post.get('commission_type')
            commission_amount = post.get('commission_amount')
            target_type = post.get('target_type')
            
            target_obj_id = request.env['target.guard'].sudo().search([('id','=',target_id)])
            print('---------------------update target guard----------',target_obj_id)
            
            # values = post 
            # values['target_id'] = int(values ['target_id'])
            # target_obj_id.sudo().write(values)
            
            if target_obj_id.target_line:
                if name:
                    target_obj_id.sudo().write({
                        'name':name.strip()
                        })
                if target_type:
                    target_obj_id.target_line.sudo().write({
                        'type':target_type
                        })
        
                if from_date:
                    target_obj_id.sudo().write({
                        'from_date':from_date
                        })
                if to_date:
                    target_obj_id.sudo().write({
                        'to_date':to_date
                        })
                if target_amount:
                    target_obj_id.target_line.sudo().write({
                        'target_amount':target_amount
                    })
                if commission_type:
                    target_obj_id.target_line.sudo().write({
                        'commission_type':commission_type
                    })
                if commission_amount:
                    target_obj_id.target_line.sudo().write({
                        'commission_amount':commission_amount
                    })
                
                target_data ={
                    
                    'id':target_obj_id.id,
                    'name': {'id':target_obj_id.id , 'name':target_obj_id.name}  if target_obj_id.name else '',
                    'from_date':fields.Datetime.to_string(target_obj_id.from_date), 
                    'to_date':fields.Datetime.to_string(target_obj_id.to_date),  
                    'target_amount':target_obj_id.target_line.target_amount if target_obj_id.target_line.target_amount else '',
                    'commission_type':target_obj_id.target_line.commission_type if target_obj_id.target_line.commission_type else '',
                    'commission_amount':target_obj_id.target_line.commission_amount if target_obj_id.target_line.commission_amount else '',
                    'target_type':{'id':target_obj_id.target_line.target_type if target_obj_id.target_line.target_type else '' , 'name':dict(target_obj_id.target_line._fields['type'].selection).get(target_obj_id.target_line.target_type) if target_obj_id.target_line.target_type else ''},

                    }
                status = True
                message = 'Success'
                code = 200
            else:
                status = False
                message = 'No Target'
                code = 400

            vals = {
                'data' : [target_data],
                'status':status,
                'message':message,
                'error_code':code
            }
            return Response(json.dumps(vals),headers=headers)
        except Exception as e:
            return Response(json.dumps({'message': e.__str__(), 'error_code': 500, 'status': False, 'data': {}}), headers=headers)
        
        
    @http.route('/create_target_deatails', type='http', auth='public', methods=['POST'], csrf=False)
    def create_target_deatails(self , **post):
        headers={'content-type':'application/json'} 
        print('-----------dddddddddddddd--------------')
        status = True
        message=''
        code = 0
        try:
            target_deatails_id = ''
            target_id =  (post.get('target_id'))
            name=post.get('name')
            target_type = post.get('target_type')
            date_from = post.get('date_form')
            to_date = post.get('to_date')
            target_amount = post.get('target_amount')
            commission_type = post.get('commission_type')
            commission_amount = post.get('commission_amount')
        
            if target_id:
                target_obj_id = request.env['target.guard'].sudo().search([('id','=',target_id)])
                print('----------------------------------------')
                
                if target_obj_id.target_line:
                        target_deatails_id = request.env['target.guard'].sudo().create({
                        
                            'target_obj_id':target_obj_id.id,
                            'name':name.strip(),
                            'date_from':date_from,
                            'to_date': to_date,
                            'target_type' : target_type,
                            'target_amount':target_amount,
                            'commission_type':commission_type,
                            'commission_amount':commission_amount
                            })
                        print('----------------------------------------')
                        
                        if target_deatails_id:
                        
                                target_data = {
                                    'id': target_deatails_id.id,
                                    'name':target_obj_id.name,
                                    'data_form':fields.Datetime.to_string(target_obj_id.from_date),
                                    'to_date':fields.Datetime.to_string(target_obj_id.to_date),
                                    'type':{'id':target_obj_id.target_line.target_type if target_obj_id.target_line.target_type else '' , 'name':dict(target_obj_id.target_line._fields['type'].selection).get(target_obj_id.target_line.target_type) if target_obj_id.target_line.target_type else ''}, 
                                    'target_amount': target_obj_id.target_line.target_amount,
                                    'commission_type':target_obj_id.target_line.commission_type,
                                    'commission_amount':target_obj_id.target_line.commission_amount
                                }
                        print('----------------------------------------')
                        status = True
                        message = 'Success'
                        code = 200
                else:
                        status = False
                        message = 'Target Not Found'
                        code = 400
                        
            vals = {
				'data' : [target_data],
				'status':status,
				'message':message,
				'error_code':code
			}            
            return Response(json.dumps(vals),headers=headers)
        except Exception as e:
            return Response(json.dumps({'message': e.__str__() ,'error_code':500 , 'status':False , 'data':{}}),headers=headers)     
        
        
        
        
            

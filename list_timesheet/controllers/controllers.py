# -*- coding: utf-8 -*-
# from odoo import http


# class ListTimesheet(http.Controller):
#     @http.route('/list_timesheet/list_timesheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/list_timesheet/list_timesheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('list_timesheet.listing', {
#             'root': '/list_timesheet/list_timesheet',
#             'objects': http.request.env['list_timesheet.list_timesheet'].search([]),
#         })

#     @http.route('/list_timesheet/list_timesheet/objects/<model("list_timesheet.list_timesheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('list_timesheet.object', {
#             'object': obj
#         })

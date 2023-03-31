# -*- coding: utf-8 -*-
# from odoo import http


# class WorksiteSheet(http.Controller):
#     @http.route('/worksite_sheet/worksite_sheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/worksite_sheet/worksite_sheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('worksite_sheet.listing', {
#             'root': '/worksite_sheet/worksite_sheet',
#             'objects': http.request.env['worksite_sheet.worksite_sheet'].search([]),
#         })

#     @http.route('/worksite_sheet/worksite_sheet/objects/<model("worksite_sheet.worksite_sheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('worksite_sheet.object', {
#             'object': obj
#         })

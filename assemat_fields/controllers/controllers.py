# -*- coding: utf-8 -*-
# from odoo import http


# class AssematFields(http.Controller):
#     @http.route('/assemat_fields/assemat_fields', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/assemat_fields/assemat_fields/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('assemat_fields.listing', {
#             'root': '/assemat_fields/assemat_fields',
#             'objects': http.request.env['assemat_fields.assemat_fields'].search([]),
#         })

#     @http.route('/assemat_fields/assemat_fields/objects/<model("assemat_fields.assemat_fields"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('assemat_fields.object', {
#             'object': obj
#         })

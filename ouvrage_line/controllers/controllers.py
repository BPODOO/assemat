# -*- coding: utf-8 -*-
# from odoo import http


# class OuvrageLine(http.Controller):
#     @http.route('/ouvrage_line/ouvrage_line', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ouvrage_line/ouvrage_line/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ouvrage_line.listing', {
#             'root': '/ouvrage_line/ouvrage_line',
#             'objects': http.request.env['ouvrage_line.ouvrage_line'].search([]),
#         })

#     @http.route('/ouvrage_line/ouvrage_line/objects/<model("ouvrage_line.ouvrage_line"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ouvrage_line.object', {
#             'object': obj
#         })

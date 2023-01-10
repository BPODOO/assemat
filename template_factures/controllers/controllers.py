# -*- coding: utf-8 -*-
# from odoo import http


# class TemplateFactures(http.Controller):
#     @http.route('/template_factures/template_factures', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/template_factures/template_factures/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('template_factures.listing', {
#             'root': '/template_factures/template_factures',
#             'objects': http.request.env['template_factures.template_factures'].search([]),
#         })

#     @http.route('/template_factures/template_factures/objects/<model("template_factures.template_factures"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('template_factures.object', {
#             'object': obj
#         })

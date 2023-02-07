# -*- coding: utf-8 -*-
# from odoo import http


# class TemplateDevis(http.Controller):
#     @http.route('/template_devis/template_devis', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/template_devis/template_devis/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('template_devis.listing', {
#             'root': '/template_devis/template_devis',
#             'objects': http.request.env['template_devis.template_devis'].search([]),
#         })

#     @http.route('/template_devis/template_devis/objects/<model("template_devis.template_devis"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('template_devis.object', {
#             'object': obj
#         })

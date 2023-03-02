# -*- coding: utf-8 -*-
# from odoo import http


# class AnnexeDevis(http.Controller):
#     @http.route('/annexe_devis/annexe_devis', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/annexe_devis/annexe_devis/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('annexe_devis.listing', {
#             'root': '/annexe_devis/annexe_devis',
#             'objects': http.request.env['annexe_devis.annexe_devis'].search([]),
#         })

#     @http.route('/annexe_devis/annexe_devis/objects/<model("annexe_devis.annexe_devis"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('annexe_devis.object', {
#             'object': obj
#         })

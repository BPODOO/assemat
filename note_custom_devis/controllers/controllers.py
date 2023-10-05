# -*- coding: utf-8 -*-
# from odoo import http


# class NoteCustomDevis(http.Controller):
#     @http.route('/note_custom_devis/note_custom_devis', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/note_custom_devis/note_custom_devis/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('note_custom_devis.listing', {
#             'root': '/note_custom_devis/note_custom_devis',
#             'objects': http.request.env['note_custom_devis.note_custom_devis'].search([]),
#         })

#     @http.route('/note_custom_devis/note_custom_devis/objects/<model("note_custom_devis.note_custom_devis"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('note_custom_devis.object', {
#             'object': obj
#         })

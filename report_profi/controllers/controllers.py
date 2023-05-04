# -*- coding: utf-8 -*-
# from odoo import http


# class ReportProfi(http.Controller):
#     @http.route('/report_profi/report_profi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_profi/report_profi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_profi.listing', {
#             'root': '/report_profi/report_profi',
#             'objects': http.request.env['report_profi.report_profi'].search([]),
#         })

#     @http.route('/report_profi/report_profi/objects/<model("report_profi.report_profi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_profi.object', {
#             'object': obj
#         })

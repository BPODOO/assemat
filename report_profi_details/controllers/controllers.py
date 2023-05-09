# -*- coding: utf-8 -*-
# from odoo import http


# class ReportProfiDetails(http.Controller):
#     @http.route('/report_profi_details/report_profi_details', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_profi_details/report_profi_details/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_profi_details.listing', {
#             'root': '/report_profi_details/report_profi_details',
#             'objects': http.request.env['report_profi_details.report_profi_details'].search([]),
#         })

#     @http.route('/report_profi_details/report_profi_details/objects/<model("report_profi_details.report_profi_details"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_profi_details.object', {
#             'object': obj
#         })

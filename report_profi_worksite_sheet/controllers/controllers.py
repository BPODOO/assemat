# -*- coding: utf-8 -*-
# from odoo import http


# class ReportProfiWorksiteSheet(http.Controller):
#     @http.route('/report_profi_worksite_sheet/report_profi_worksite_sheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_profi_worksite_sheet/report_profi_worksite_sheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_profi_worksite_sheet.listing', {
#             'root': '/report_profi_worksite_sheet/report_profi_worksite_sheet',
#             'objects': http.request.env['report_profi_worksite_sheet.report_profi_worksite_sheet'].search([]),
#         })

#     @http.route('/report_profi_worksite_sheet/report_profi_worksite_sheet/objects/<model("report_profi_worksite_sheet.report_profi_worksite_sheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_profi_worksite_sheet.object', {
#             'object': obj
#         })

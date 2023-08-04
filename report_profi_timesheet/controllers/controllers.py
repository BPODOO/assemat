# -*- coding: utf-8 -*-
# from odoo import http


# class ReportProfiTimesheet(http.Controller):
#     @http.route('/report_profi_timesheet/report_profi_timesheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_profi_timesheet/report_profi_timesheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_profi_timesheet.listing', {
#             'root': '/report_profi_timesheet/report_profi_timesheet',
#             'objects': http.request.env['report_profi_timesheet.report_profi_timesheet'].search([]),
#         })

#     @http.route('/report_profi_timesheet/report_profi_timesheet/objects/<model("report_profi_timesheet.report_profi_timesheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_profi_timesheet.object', {
#             'object': obj
#         })

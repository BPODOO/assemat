# -*- coding: utf-8 -*-
# from odoo import http


# class ReportTimesheet(http.Controller):
#     @http.route('/report_timesheet/report_timesheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_timesheet/report_timesheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_timesheet.listing', {
#             'root': '/report_timesheet/report_timesheet',
#             'objects': http.request.env['report_timesheet.report_timesheet'].search([]),
#         })

#     @http.route('/report_timesheet/report_timesheet/objects/<model("report_timesheet.report_timesheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_timesheet.object', {
#             'object': obj
#         })

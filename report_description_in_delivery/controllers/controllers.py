# -*- coding: utf-8 -*-
# from odoo import http


# class ReportDescriptionInDelivery(http.Controller):
#     @http.route('/report_description_in_delivery/report_description_in_delivery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_description_in_delivery/report_description_in_delivery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_description_in_delivery.listing', {
#             'root': '/report_description_in_delivery/report_description_in_delivery',
#             'objects': http.request.env['report_description_in_delivery.report_description_in_delivery'].search([]),
#         })

#     @http.route('/report_description_in_delivery/report_description_in_delivery/objects/<model("report_description_in_delivery.report_description_in_delivery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_description_in_delivery.object', {
#             'object': obj
#         })

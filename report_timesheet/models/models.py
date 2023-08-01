# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class report_timesheet(models.Model):
#     _name = 'report_timesheet.report_timesheet'
#     _description = 'report_timesheet.report_timesheet'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class template_devis(models.Model):
#     _name = 'template_devis.template_devis'
#     _description = 'template_devis.template_devis'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

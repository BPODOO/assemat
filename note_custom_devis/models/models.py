# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class note_custom_devis(models.Model):
#     _name = 'note_custom_devis.note_custom_devis'
#     _description = 'note_custom_devis.note_custom_devis'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

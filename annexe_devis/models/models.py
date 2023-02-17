# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class annexe_devis(models.Model):
#     _name = 'annexe_devis.annexe_devis'
#     _description = 'annexe_devis.annexe_devis'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

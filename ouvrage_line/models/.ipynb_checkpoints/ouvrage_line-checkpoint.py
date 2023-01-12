# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OuvrageLine(models.Model):
    _name = 'ouvrage.line'
    _description = """Ligne(s) d'ouvrage(s)"""

    name = fields.Char(string='Name')
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line')
    
    bp_fabrication_ids = fields.One2many('fabrication', 'bp_ouvrage_line_id', string='Fabrication')
    bp_material_line_ids = fields.One2many('material.line', 'bp_ouvrage_line_id', string='Material Lines')
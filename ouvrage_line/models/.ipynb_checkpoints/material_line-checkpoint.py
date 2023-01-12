# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialLine(models.Model):
    _name = 'material.line'
    _description = """Ligne(s) du matériel"""
    
    name = fields.Char(string='Name')
    
    bp_cost = fields.Float(string='Cost')
    bp_cost_unit = fields.Float(string='Cost Unit')
    
    bp_qty = fields.Float(string='Quantity')
    bp_product_id = fields.Many2one('product.product', string='Product')
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string='Ouvrage Line')
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialLine(models.Model):
    _name = 'material.line'
    _description = """Ligne(s) du matériel"""
    
    name = fields.Char(string='Name')
    
    bp_cost = fields.Float(string='Coût')
    bp_cost_unit = fields.Float(string='Coût unitaire')
    
    bp_qty = fields.Float(string='Quantité')
    bp_product_id = fields.Many2one('product.product', string='Article')
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Bon de commande')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Ligne de vente')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string="Ligne d'ouvrage")
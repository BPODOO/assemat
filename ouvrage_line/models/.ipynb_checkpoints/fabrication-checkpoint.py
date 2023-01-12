# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Fabrication(models.Model):
    _name = 'fabrication'
    _description = """Fabrication d'une ligne d'ouvrage"""
    
    name = fields.Char(string='Name')
    
    bp_cost = fields.Float(string='Cost')
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line')
    
    bp_duration = fields.Float(string='Duration')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string='Ouvrage Line')
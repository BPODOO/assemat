# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialLine(models.Model):
    _name = 'material.line'
    _description = """Ligne(s) du matériel"""
    
    name = fields.Char(string='Nom')
    
    bp_cost = fields.Float(string='Coût', compute="_compute_cost")
    bp_cost_unit = fields.Float(string='Coût unitaire')
    
    bp_qty = fields.Float(string='Quantité')
    bp_product_id = fields.Many2one('product.product', string='Article')
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Bon de commande')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Ligne de vente')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string="Ligne d'ouvrage")
    
    @api.depends('bp_qty','bp_cost_unit')
    def _compute_cost(self):
        for record in self:
            record.bp_cost = record.bp_cost_unit * record.bp_qty
        
    @api.onchange('bp_product_id')
    def _onchange_product(self):
        for record in self:
            record.bp_cost_unit = record.bp_product_id.standard_price
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialLine(models.Model):
    _name = 'material.line'
    _description = """Ligne(s) du matériel"""
    
    name = fields.Char(string='Nom', compute="_compute_name")
    
    bp_cost = fields.Float(string='Coût', compute="_compute_cost", store=True)
    bp_cost_unit = fields.Float(string='Coût unitaire')
    
    bp_qty = fields.Float(string='Quantité')
    bp_product_id = fields.Many2one('product.product', string='Article', required=True)
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Bon de commande')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Ligne de vente')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string="Ligne d'ouvrage", ondelete='cascade')
    
    @api.depends('bp_product_id')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.bp_product_id.name}'
    
    @api.depends('bp_qty','bp_cost_unit')
    def _compute_cost(self):
        for record in self:
            record.bp_cost = record.bp_cost_unit * record.bp_qty
        
    @api.onchange('bp_product_id')
    def _onchange_product(self):
        for record in self:
            record.bp_cost_unit = record.bp_product_id.standard_price
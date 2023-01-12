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
    
    bp_selling_price = fields.Float(string="Prix de vente", compute="_compute_selling_price")
    bp_cost_price = fields.Float(string="Prix de revient", compute="_compute_cost_price")
    
    bp_forecast_margin = fields.Float(string="Marge prévisionnelle", compute="_compute_forecast_margin")
    
    @api.depends('bp_material_line_ids','bp_fabrication_ids')
    def _compute_cost_price(self):
        self.bp_cost_price = sum(self.bp_material_line_ids.mapped('bp_cost')) + sum(self.bp_fabrication_ids.mapped('bp_cost')) + self.bp_sale_order_id.bp_transport_cost
        
    
    @api.depends('bp_material_line_ids','bp_fabrication_ids')
    def _compute_selling_price(self):
        sum_material = sum(self.bp_material_line_ids.mapped('bp_cost'))
        sum_fabrication = sum(self.bp_fabrication_ids.mapped('bp_cost'))
        
        self.bp_selling_price = (sum_material * self.bp_sale_order_id.bp_coefficient) + (sum_fabrication * self.bp_sale_order_id.bp_coefficient) + sum_fabrication + (self.bp_sale_order_id.bp_transport_cost * self.bp_sale_order_id.bp_coefficient)
        
    @api.depends('bp_selling_price','bp_cost_price')
    def _compute_forecast_margin(self):
        self.bp_forecast_margin = self.bp_selling_price - self.bp_cost_price
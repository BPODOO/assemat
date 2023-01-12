# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class OuvrageLine(models.Model):
    _name = 'ouvrage.line'
    _description = """Ligne(s) d'ouvrage(s)"""

    name = fields.Char(string='Nom', compute="_compute_name")
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line')
    
    bp_coefficient = fields.Float(related='bp_sale_order_id.bp_coefficient')
    bp_hourly_rate = fields.Float(related='bp_sale_order_id.bp_hourly_rate')
    bp_transport_cost = fields.Float(related='bp_sale_order_id.bp_transport_cost')
    
    bp_fabrication_ids = fields.One2many('fabrication', 'bp_ouvrage_line_id', string='Fabrication')
    bp_material_line_ids = fields.One2many('material.line', 'bp_ouvrage_line_id', string='Material Lines')
    
    bp_selling_price = fields.Float(string="Prix de vente", compute="_compute_selling_price")
    bp_cost_price = fields.Float(string="Prix de revient", compute="_compute_cost_price")
    
    bp_forecast_margin = fields.Float(string="Marge prévisionnelle", compute="_compute_forecast_margin")
    
    
    @api.depends('bp_sale_order_id','bp_sale_order_line_id')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.bp_sale_order_id.name} - {record.bp_sale_order_line_id.id}'
    
    @api.depends('bp_material_line_ids','bp_fabrication_ids')
    def _compute_cost_price(self):
        for record in self:
            record.bp_cost_price = sum(record.bp_material_line_ids.mapped('bp_cost')) + sum(record.bp_fabrication_ids.mapped('bp_cost')) + record.bp_sale_order_id.bp_transport_cost
        
    
    @api.depends('bp_material_line_ids','bp_fabrication_ids')
    def _compute_selling_price(self):
        for record in self:
            sum_material = sum(record.bp_material_line_ids.mapped('bp_cost'))
            sum_fabrication = sum(record.bp_fabrication_ids.mapped('bp_cost'))

            record.bp_selling_price = (sum_material * record.bp_sale_order_id.bp_coefficient) + (sum_fabrication * record.bp_sale_order_id.bp_coefficient) + sum_fabrication + (record.bp_sale_order_id.bp_transport_cost * record.bp_sale_order_id.bp_coefficient)
        
    @api.depends('bp_selling_price','bp_cost_price')
    def _compute_forecast_margin(self):
        for record in self:
            record.bp_forecast_margin = record.bp_selling_price - record.bp_cost_price
    
    
    def action_save(self):
        ##ICI RETOURNE LE PRIX SUR LA LIGNE DE VENTE
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}
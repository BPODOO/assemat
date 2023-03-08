# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class OuvrageLine(models.Model):
    _name = 'ouvrage.line'
    _description = """Ligne(s) d'ouvrage(s)"""

    name = fields.Char(string='Nom', compute="_compute_name")
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Bon de commande', readonly=True)
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Ligne de vente', ondelete='cascade', readonly=True)
    
    bp_coefficient_material = fields.Float(related='bp_sale_order_id.bp_coefficient_material', help="Coefficient matériel du devis")
    bp_coefficient_manufacturing = fields.Float(related='bp_sale_order_id.bp_coefficient_manufacturing', help="Coefficient fabrication du devis")
    bp_hourly_rate = fields.Float(related='bp_sale_order_id.bp_hourly_rate', help="Taux horaire du devis")
    
    bp_fabrication_ids = fields.One2many('fabrication', 'bp_ouvrage_line_id', string='Fabrication')
    bp_material_line_ids = fields.One2many('material.line', 'bp_ouvrage_line_id', string='Material Lines')
    
    bp_selling_price = fields.Float(string="Prix de vente", store=True, compute="_compute_selling_price", 
                                    help="(Somme des coûts matériels * Coeff matériel) + (Somme des coûts fabrication * Coeff fabrication)")
    
    bp_cost_price = fields.Float(string="Prix de revient", store=True, compute="_compute_cost_price", help="Somme des coûts matériels + Somme des coûts fabrication")
    
    bp_forecast_margin = fields.Float(string="Marge prévisionnelle", store=True, compute="_compute_forecast_margin", help="Prix de vente - Prix de revient")
    
    @api.onchange('bp_sale_order_line_id')
    def _onchange_use_ouvrage(self):
        for record in self:
            record.bp_sale_order_line_id.bp_use_ouvrage = True if record.bp_sale_order_line_id else False
    
    @api.depends('bp_sale_order_id','bp_sale_order_line_id')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.bp_sale_order_id.name} - {record.bp_sale_order_line_id.id}'
    
    @api.depends('bp_material_line_ids','bp_fabrication_ids')
    def _compute_cost_price(self):
        for record in self:
            record.bp_cost_price = sum(record.bp_material_line_ids.mapped('bp_cost')) + sum(record.bp_fabrication_ids.mapped('bp_cost'))
        
    @api.depends('bp_material_line_ids','bp_fabrication_ids')
    def _compute_selling_price(self):
        for record in self:
            sum_material = sum(record.bp_material_line_ids.mapped('bp_cost'))
            sum_fabrication = sum(record.bp_fabrication_ids.mapped('bp_cost'))

            record.bp_selling_price = (sum_material * record.bp_sale_order_id.bp_coefficient_material) + (sum_fabrication * record.bp_sale_order_id.bp_coefficient_manufacturing)
        
    @api.depends('bp_selling_price','bp_cost_price')
    def _compute_forecast_margin(self):
        for record in self:
            record.bp_forecast_margin = record.bp_selling_price - record.bp_cost_price
        
    #OVERIDE
    def unlink(self):
        for record in self:
            record.bp_sale_order_line_id.bp_use_ouvrage = False
        return super(OuvrageLine, self).unlink()
    
    def _save_price(self):
        self.ensure_one()
        self.bp_sale_order_line_id.price_unit = self.bp_selling_price
    
    #SAVE ET RETOURNE LE PRIX SUR LA LIGNE
    def action_save(self):
        self.ensure_one()
        self.bp_sale_order_line_id.price_unit = self.bp_selling_price
        return {'type': 'ir.actions.act_window_close'}
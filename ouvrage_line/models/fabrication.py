# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Fabrication(models.Model):
    _name = 'fabrication'
    _description = """Fabrication d'une ligne d'ouvrage"""
    
    name = fields.Char(string='Nom', required=True)
    
    bp_cost = fields.Float(string='Coût', compute="_compute_cost", store=True)
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Bon de commande')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Ligne de vente')

    bp_unit_duration = fields.Float(string="Durée unitaire", help="Durée unitaire de la prestation")
    bp_qty = fields.Float(string="Quantité", default=0)
    
    bp_duration = fields.Float(string='Durée totale', store=True, compute="_compute_duration", help="Durée totale de la prestation [Durée unitaire * Quantité]")
    
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string="Ligne d'ouvrage", ondelete='cascade')
    
    bp_timesheet_description_id = fields.Many2one('timesheet.description', string="Prestation")
            
    @api.onchange('bp_timesheet_description_id')
    def _onchange_timesheet_description_id(self):
        for record in self:
            record.update({
                            'name': record.bp_timesheet_description_id.name,
                            'bp_unit_duration': record.bp_timesheet_description_id.bp_default_time,
                          })

    @api.depends('bp_unit_duration','bp_qty')
    def _compute_duration(self):
        for record in self:
            record.bp_duration = (record.bp_unit_duration * record.bp_qty)
            
    
    @api.depends('bp_duration')
    def _compute_cost(self):
        for record in self:
            record.bp_cost = (record.bp_duration * record.bp_sale_order_id.bp_hourly_rate)
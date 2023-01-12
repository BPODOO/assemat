# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class Fabrication(models.Model):
    _name = 'fabrication'
    _description = """Fabrication d'une ligne d'ouvrage"""
    
    name = fields.Char(string='Nom', required=True)
    
    bp_cost = fields.Float(string='Coût', compute="_compute_cost")
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Bon de commande')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Ligne de vente')
    
    bp_duration = fields.Float(string='Durée')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string="Ligne d'ouvrage")
    
    @api.depends('bp_duration')
    def _compute_cost(self):
        for record in self:
            record.bp_cost = (record.bp_duration * record.bp_sale_order_id.bp_hourly_rate) * record.bp_sale_order_id.bp_coefficient
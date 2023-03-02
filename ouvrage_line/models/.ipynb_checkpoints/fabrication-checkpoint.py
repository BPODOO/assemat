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
    
    bp_duration = fields.Float(string='Durée')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string="Ligne d'ouvrage", ondelete='cascade')
    
    bp_list_desc = fields.Selection(
        selection='_get_original_field_options',
        string='Prestation'
    )

    def _get_original_field_options(self):
        _logger.info("ici")
        return self.env['account.analytic.line']._fields['bp_list_desc'].selection

    @api.onchange('bp_list_desc')
    def _onchange_prestation(self):
        for record in self:
            record.name = dict(self.env['account.analytic.line']._fields['bp_list_desc'].selection).get(record.bp_list_desc)
    
    @api.depends('bp_duration')
    def _compute_cost(self):
        for record in self:
            record.bp_cost = (record.bp_duration * record.bp_sale_order_id.bp_hourly_rate)
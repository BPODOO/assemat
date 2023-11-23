# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class MaterialLine(models.Model):
    _name = 'material.line'
    _description = """Ligne(s) du matériel"""
    
    name = fields.Char(string='Nom', compute="_compute_name")
    bp_characteristic = fields.Char(string='Caractéristique')
    
    bp_cost = fields.Float(string='Coût prévi', compute="_compute_cost", store=True)
    bp_cost_actual = fields.Float(string='Coût actuel', compute="_compute_cost_actual", store=True)
    bp_cost_unit = fields.Float(string='Coût unit')
    bp_cost_unit_real = fields.Float(string='Coût unit réel', default=0, store=True)
    
    bp_qty = fields.Float(string='Qté prévue')
    bp_qty_used = fields.Float(string="Qté utilisée")
    
    bp_availability = fields.Selection([('in_stock','En stock'),('ordered','Commandé'),('to_order','À commander')], string="Disponibilité")
    
    bp_product_id = fields.Many2one('product.product', string='Article', required=True)
    
    bp_sale_order_id = fields.Many2one('sale.order', string='Bon de commande')
    bp_sale_order_line_id = fields.Many2one('sale.order.line', string='Ligne de vente')
    
    bp_ouvrage_line_id = fields.Many2one('ouvrage.line', string="Ligne d'ouvrage", ondelete='cascade')
    
    bp_unpredictable_line = fields.Boolean(string="Non prévue", default=False)
    
    #OVERIDE CREATE
    @api.model
    def create(self, vals_list):
        res = super(MaterialLine, self).create(vals_list)
        #Vérification si la création se fait depuis sale.order / project.project
        #Assignation automatique au groupe
        if(self.env.context.get('active_model') == 'project.project'):
            if(self._context.get('default_bp_sale_order_line_id')):
                res.update({
                    'bp_ouvrage_line_id': self.env['ouvrage.line'].search([('bp_sale_order_line_id','=',self._context['default_bp_sale_order_line_id'])]).id,
                    'bp_sale_order_id': self.env['sale.order.line'].browse(self._context['default_bp_sale_order_line_id']).order_id.id,
                    'bp_sale_order_line_id': self._context['default_bp_sale_order_line_id'],
                    'bp_unpredictable_line': True,
                })
                res._onchange_product()
            return res
        else:
            return res
    
    @api.depends('bp_product_id')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.bp_product_id.name}'
    
    @api.depends('bp_qty','bp_cost_unit')
    def _compute_cost(self):
        for record in self:
            record.bp_cost = record.bp_cost_unit * record.bp_qty
    
    @api.depends('bp_qty_used','bp_cost_unit_real')
    def _compute_cost_actual(self):
        for record in self:
            if record.bp_cost_unit_real != 0.0:
                record.bp_cost_actual = record.bp_cost_unit_real * record.bp_qty_used
            else:
                record.bp_cost_actual = record.bp_cost_unit * record.bp_qty_used
        
    
    @api.onchange('bp_product_id')
    def _onchange_product(self):
        for record in self:
            record.bp_cost_unit = record.bp_product_id.standard_price
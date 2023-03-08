# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'
    
    bp_sale_order_ids = fields.One2many('sale.order', 'bp_worksite', string="Bon de commande(s)", readonly=True)
    
    allocated_hours = fields.Float(compute='_compute_hours', store=True, readonly=False, copy=False)
    
    @api.depends('bp_sale_order_ids')
    def _compute_hours(self):
        _logger.info("ici")
        orders = self.bp_sale_order_ids.filtered(lambda x: x.state == 'sale')
        # self.allocated_hours = sum
        _logger.info(orders)
        sale_lines = orders.mapped('order_line')
        _logger.info(sale_lines)
        # return
    
    
    def action_open_material_lines_associated(self):
        view_id = self.env.ref('ouvrage_line.material_line_associated_tree_bp').id
        order_ids = self.env['sale.order'].search([('bp_worksite','=',self.id),('state','=','sale')]).ids
        action = { 
                    'type': 'ir.actions.act_window', 
                    'name': 'Suivi matériel', 
                    'view_type': 'form',
                    'views': [[view_id, 'tree']],
                    'view_mode': 'tree,form',
                    'target': 'current',
                    'context': {'group_by': ['bp_sale_order_line_id']},
                    'res_model': 'material.line',
                    'domain': [('bp_sale_order_id.id','in', order_ids)]
                 }
        return action
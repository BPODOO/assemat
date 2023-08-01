# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'
    
    bp_allocated_hours = fields.Float(string="Temps des fabrications", readonly=False, copy=False, store=True, compute="_compute_bp_allocated_hours")
    
    @api.depends('bp_sale_order_ids.order_line.bp_ouvrage_line.bp_fabrication_ids.bp_duration','bp_sale_order_ids.state')
    def _compute_bp_allocated_hours(self):
        for record in self:
            orders = record.bp_sale_order_ids.filtered(lambda x: x.state == 'sale')
            record.bp_allocated_hours = sum(orders.mapped('order_line.bp_ouvrage_line.bp_fabrication_ids.bp_duration'))
            record.allocated_hours = record.bp_allocated_hours

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
                    'context': {'group_by': ['bp_sale_order_line_id'], 'default_bp_unpredictable_line': True},
                    'res_model': 'material.line',
                    'domain': [('bp_sale_order_id.id','in', order_ids)]
                 }
        return action
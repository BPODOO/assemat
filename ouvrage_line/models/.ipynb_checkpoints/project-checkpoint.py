# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'
    
    
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
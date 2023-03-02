# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'
    
    
    def action_open_material_lines_associated(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ouvrage_line.material_lines_action_open_associated")
        order_ids = self.env['sale.order'].search([('bp_worksite','=',self.id),('state','=','sale')]).ids
        action['context'] = {
            'flags': {'hasSelectors': False},
            'group_by': 'bp_sale_order_line_id',
            'search_default_bp_sale_order_id':  [order_ids],
        }
        return action


    
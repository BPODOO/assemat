# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import json

import logging
_logger = logging.getLogger(__name__)

class PrintWorksiteSheet(models.TransientModel):
    _name = "print.worksite.sheet"
    _description = "Ligne(s) de vente a imprimé"
    
    bp_project_id = fields.Many2one('project.project')
    bp_order_id = fields.Many2one('sale.order', domain="[('id','in',bp_order_domain_ids)]")
    
    bp_order_domain_ids = fields.Many2many('sale.order', readonly=True)
    
    bp_res_id = fields.Integer('Related Document ID')
    bp_order_line = fields.One2many('sale.order.line', compute="_get_lines", readonly=False)
    bp_select_all_lines = fields.Boolean(string="Toutes les lignes", default=False)
    
    bp_auto_complete_section= fields.Boolean(string="Auto sélection section")
    bp_detect_sections = fields.Boolean()
    
    def action_print_report_worksite(self):
        sale_lines = self.bp_order_line.filtered(lambda x: x.bp_is_select_bis is True)
        
        #Impossible de faire passer les données ici elles sont directement en string... ou alors json.dumps
        data = {
            'data': {
                 'objet_section': self.list_sections(self.bp_order_line),
                 'sale_order_id': self.bp_order_id.id,
                 'sale_line_ids': sale_lines.ids,
                 'ouvrage_line_ids': sale_lines.bp_ouvrage_line.ids, #Depuis l'ouvrage on peut obtenir toutes les informations qu'on souhaite Materiel, Fabrications ...
                 'project_id': self.bp_project_id.id, 
            }
        }
        
        # self._clean_lines() #Clean si close_on_report_download = True
        action = self.env.ref('worksite_sheet.action_report_worksite_sheet').report_action(None, data=data)
        action.update({'close_on_report_download': False})
        return action
 
    def list_sections(self, sale_line_wizard):
        cpt = 0
        objet_sections = {}
        for section in sale_line_wizard:
            if section.display_type == "line_section" and section.bp_is_select:
                objet_sections[ cpt if cpt == 0 else cpt-1] = section.name
            cpt += 1
        return objet_sections
    
    def detect_sections(self, sale_line):
        flag = True
        for section in sale_line:
            if section.display_type == "line_section":
                flag = False
        return flag
        
    
    def select_all_lines(self):
        is_selected = not self.bp_select_all_lines
        for line in self.bp_order_line:
            line.bp_is_select = is_selected
            line.bp_is_select_bis = is_selected
        self.bp_select_all_lines = is_selected

        view_id = self.env.ref('worksite_sheet.view_print_worksite_sheet_bp').id
        return {
            'name': 'Fiche de chantier',
            'type': 'ir.actions.act_window',
            'res_model': 'print.worksite.sheet',
            'res_id': self.id,
            'context': {
                'default_bp_order_domain_ids': self.bp_order_domain_ids.ids,
                'default_bp_order_id': self.bp_order_id.id,
                'default_bp_select_all_lines': self.bp_select_all_lines,
                'default_bp_project_id': self.bp_project_id.id,
            },
            'target': 'new',
            'view_id': view_id,
            'view_mode': 'form',
        }
    
    @api.depends('bp_order_id')
    def _get_lines(self):
        self.write({'bp_order_line': [(6, 0, self.bp_order_id.order_line.ids)]})
        sections_in = self.detect_sections(self.bp_order_id.order_line)
        self.write({'bp_detect_sections': sections_in})

    @api.onchange('bp_order_id')
    def _onchange_auto_complete_section(self):
        self._clean_lines()
    
    @api.onchange('bp_order_line')
    def _onchange_is_select(self):
        flag = False
        for line in self.bp_order_line:
            if self.bp_auto_complete_section:
                if line.display_type == "line_section":
                    flag = line.bp_is_select
                    line.update({
                        'bp_is_select': line.bp_is_select,
                        'bp_is_select_bis': line.bp_is_select,
                        })
                    line.bp_reload = not line.bp_reload
                else:
                    line.update({
                        'bp_is_select': flag,
                        'bp_is_select_bis': flag,
                        })
                    line._origin.bp_is_select_bis = flag
                    line.bp_reload = not line.bp_reload
            else:
                line._origin.bp_is_select_bis = line.bp_is_select
            
    def _clean_lines(self):
        for line in self.bp_order_id.order_line:
            line.bp_is_select = False
            line.bp_is_select_bis = False
            
    #Refresh les lignes select et ferme la page
    def close_button(self):
        self._clean_lines()
        return {'type': 'ir.actions.act_window_close'}
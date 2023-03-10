# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

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
    
    def action_print_report_worksite(self):
        _logger.info(self.bp_order_line.filtered(lambda x: x.bp_is_select is True))
        sale_lines = self.bp_order_line.filtered(lambda x: x.bp_is_select is True)
        data = {
            'data': {
                'custom_data': 'Value One',
                'data_two': 123,
                'data_three': ['List Item 1', 'List Item 2', 'List Item 3'],
            }
           
        }
        # Appeler la fonction print_report() avec les données
        # return self.env['report'].get_action(self, 'worksite_sheet.action_report_worksite_sheet', data=data)
        self._clean_lines()
        action = self.env.ref('worksite_sheet.action_report_worksite_sheet').report_action(None, data=data)
        action.update({'close_on_report_download': False})
        return action
#         active_ids = self.env['sale.order'].search([('id','in',self.env.context.get('active_ids', []))])
        
#         if(len(active_ids) >= 2):
#             raise UserError('Cette action ne gère pas la copie venant de plusieurs Devis')

#         targetSale = self.env['sale.order'].browse(self.order_id.id)
#         sale = self.env['sale.order'].browse(self.res_id)

#         #Récupère la dernière séquence pour mettre les lignes à la suite des lignes du Devis cible
#         lastSequence = self.env['sale.order.line'].search([('order_id','=',sale.id)], order="sequence desc")[0]

# #         Les lignes qu'on traite sont seulement celle sélectionné si l'option "Sélection par ligne est active" autrement on prend toutes les lignes
#         lines = [line for line in self.order_line if line.selectable] if self.select_line else sale.order_line
        
#         for line in lines:
#             #Traitement Si Ouvrage / Section / Article simple
#             if(line.product_id.bom_ids):
#                 newSaleline = self.env['sale.order.line'].create({
#                                                                 'order_id': targetSale.id,
#                                                                 'sequence': lastSequence if lastSequence else 10,
#                                                                 'product_id': line.product_id.id,
#                                                                 'name': line.name,
#                                                                 'product_uom_qty': line.product_uom_qty,
#                                                                 'product_uom': line.product_uom.id
#                                                            })
#                 ouvragesOld = self.env['ouvrage.line'].search([('order_parent','=',sale.id),('order_parent_line','=',line.id)])
                
#                 #On supprime les lignes d'ouvrage créer, car par défaut il reprend les lignes de BOM
#                 #DELETE puis CREATE -> + rapide que de faire des conditions de recherche ou une nouvelle fonction de gestion des BOM LINES
#                 newOuvrageToDelete = self.env['ouvrage.line'].search([('order_parent','=',targetSale.id),('order_parent_line','=',newSaleline.id)])
#                 newOuvrageToDelete.unlink()
#                 for ouvrage in ouvragesOld:
#                     self.env['ouvrage.line'].create({
#                                                         'order_parent': targetSale.id,
#                                                         'order_parent_line': newSaleline.id,
#                                                         'product_id': ouvrage.product_id.id,
#                                                         'categ': ouvrage.categ,
#                                                         'qty': ouvrage.qty,
#                                                         'description': ouvrage.description,
#                                                         'cout_unit': ouvrage.cout_unit,
#                                                         'coeff_FG': ouvrage.coeff_FG,
#                                                         'coeff_VE': ouvrage.coeff_VE,
#                                                         'coeff_CO': ouvrage.coeff_CO
#                                                     })
#             elif(line.display_type):
#                 targetSale.write({'order_line': [(0,0, {'display_type': line.display_type, 'name': line.name, 'sequence': lastSequence if lastSequence else 10})]})
#             else:
#                 newSaleline = self.env['sale.order.line'].create({
#                                                                      'order_id': targetSale.id,
#                                                                      'sequence': lastSequence if lastSequence else 10,
#                                                                      'product_id': line.product_id.id,
#                                                                      'name': line.name,
#                                                                      'product_uom_qty': line.product_uom_qty,
#                                                                      'product_uom': line.product_uom.id,
#                                                                      'price_unit': line.price_unit,
#                                                                 })
#                 newSaleline.update({
#                                       'price_unit': line.price_unit
#                                   })
            
#         self.cleanSelectable()
            
#         if self._context.get('open_order', False):
#             return {
#                         'name': targetSale.name,
#                         'view_mode': 'form',
#                         'res_model': 'sale.order',
#                         'type': 'ir.actions.act_window',
#                         'res_id': targetSale.id,
#                     }
    
    
    def select_all_lines(self):
        is_selected = not self.bp_select_all_lines
        for line in self.bp_order_line:
            line.bp_is_select = is_selected
        self.bp_select_all_lines = is_selected

        view_id = self.env.ref('worksite_sheet.view_print_worksite_sheet_bp').id
        return {
            'name': 'Fiche de chantier',
            'type': 'ir.actions.act_window',
            'res_model': 'print.worksite.sheet',
            'context': {
                'default_bp_order_domain_ids': self.bp_order_domain_ids.ids,
                'default_bp_order_id': self.bp_order_id.id,
                'default_bp_select_all_lines': self.bp_select_all_lines,
                'default_bp_project_id': self.bp_project_id,
            },
            'target': 'new',
            'view_id': view_id,
            'view_mode': 'form',
        }
    
    @api.depends('bp_order_id')
    def _get_lines(self):
        self.write({'bp_order_line': [(6, 0, self.bp_order_id.order_line.ids)]})
    
    @api.onchange('bp_order_line')
    def _onchange_is_select(self):
        for line in self.bp_order_line:
            line._origin.update({
                'bp_is_select': line.bp_is_select,
            })
            
    def _clean_lines(self):
        # sale = self.env['sale.order'].browse(self.res_id)
        for line in self.bp_order_id.order_line:
            line.bp_is_select = False
            
    #Refresh les lignes select et ferme la page
    def close_button(self):
        self._clean_lines()
        return {'type': 'ir.actions.act_window_close'}
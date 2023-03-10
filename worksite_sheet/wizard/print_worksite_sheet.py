# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

import logging
_logger = logging.getLogger(__name__)

class PrintWorksiteSheet(models.TransientModel):
    _name = "print.worksite.sheet"
    _description = "Ligne(s) de vente a imprimé"
    
    bp_order_id = fields.Many2one('sale.order', domain="[('id','in',bp_order_domain_ids)]")
    
    bp_order_domain_ids = fields.Many2many('sale.order', readonly=True)
    
    bp_res_id = fields.Integer('Related Document ID')
    bp_order_line = fields.One2many('sale.order.line', compute="_get_lines", readonly=False)
    bp_select_all_lines = fields.Boolean(string="Toutes les lignes", default=False)
    
    def action_print_report_worksite(self):
        _logger.info("ici")
        _logger.info(self.bp_order_line)
        _logger.info(self.bp_order_line.filtered(lambda x: x.bp_is_select is True))
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
        
    @api.depends('bp_order_id')
    def _get_lines(self):
        self.write({'bp_order_line': [(6, 0, self.bp_order_id.order_line.ids)]})
    
    @api.onchange('bp_order_line')
    def _onchange_is_select(self):
        for line in self.bp_order_line:
            line._origin.update({
                'bp_is_select': line.bp_is_select,
            })
    
    
#     def cleanSelectable(self):
#         # sale = self.env['sale.order'].browse(self.res_id)
#         for line in self.bp_order_id.order_line:
#             line.bp_selectable = False
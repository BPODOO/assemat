# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    bp_use_ouvrage = fields.Boolean(string="Dispose d'un ouvrage", readonly=True)
    bp_task_id = fields.Many2one('project.task', string="Dispose d'une tâche", readonly=True, help="Ce champ montre la tâche assigné à cette ligne, uniquement utile pour le système d'ouvrage")
    
    bp_ouvrage_line = fields.One2many('ouvrage.line', 'bp_sale_order_line_id', string="Ouvrage", readonly=True)
    
    def action_open_ouvrage_line(self):

        if not(self): raise UserError("Sauvegarde nécéssaire en cours avant de faire un calcul des prix !")
        
        manufacturing_tasks = self._default_value_manufacturing()
        context = self.env.context.copy()
        context.update({'default_bp_sale_order_id': self.order_id.id, 'default_bp_sale_order_line_id': self.id, 
                        'default_bp_fabrication_ids': manufacturing_tasks, 
                        'default_bp_coefficient_material': self.order_id.bp_coefficient_material,
                        'default_bp_coefficient_manufacturing': self.order_id.bp_coefficient_manufacturing})
        
        ouvrage = self.env['ouvrage.line'].search([('bp_sale_order_line_id','=',self.id)])
        if(ouvrage):
            return {
                'name': "Calcul du prix de l'ouvrage",
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ouvrage.line',
                'res_id': ouvrage.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        else:
            return {
                'name': "Calcul du prix de l'ouvrage",
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ouvrage.line',
                'context': context,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        
    def action_get_ouvrage_price(self):
        ouvrage_line = self.env['ouvrage.line'].search([('bp_sale_order_line_id','=',self.id)])
        if(ouvrage_line):
            self.price_unit = ouvrage_line.bp_selling_price
            
    def _default_value_manufacturing(self):
        list_description = dict(self.env['account.analytic.line']._fields['bp_list_desc'].selection)
        manufacturing_tasks = [{'name': element} for element in list_description.values()]
        return manufacturing_tasks
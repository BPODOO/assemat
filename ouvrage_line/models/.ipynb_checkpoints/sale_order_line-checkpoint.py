# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    bp_use_ouvrage = fields.Boolean(string="Dispose d'un ouvrage", readonly=True)
    bp_active_task = fields.Boolean(string="Dispose d'une tâche", readonly=True)
    
    def action_open_ouvrage_line(self):
        manufacturing_tasks = self._default_value_manufacturing()
        context = self.env.context.copy()
        context.update({'default_bp_sale_order_id': self.order_id.id, 'default_bp_fabrication_ids': manufacturing_tasks})
        
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
        selling_price = self.env['ouvrage.line'].search([('bp_sale_order_line_id','=',self.id)]).bp_selling_price
        if(selling_price):
            self.price_unit = selling_price
            
    def _default_value_manufacturing(self):
        list_description = dict(self.env['account.analytic.line']._fields['bp_list_desc'].selection)
        manufacturing_tasks = [{'name': element} for element in list_description.values()]
        return manufacturing_tasks
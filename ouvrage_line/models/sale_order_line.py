# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    bp_use_ouvrage = fields.Boolean(string="Dispose d'un ouvrage", readonly=True)
    bp_task_id = fields.Many2one('project.task', string="Dispose d'une tâche", readonly=True, copy=False, help="Ce champ montre la tâche assigné à cette ligne, uniquement utile pour le système d'ouvrage")
    
    bp_ouvrage_line = fields.One2many('ouvrage.line', 'bp_sale_order_line_id', string="Ouvrage", readonly=True)
    bp_material_line_ids = fields.One2many('material.line', 'bp_sale_order_line_id', string="Matériel(s)", readonly=True)
    bp_fab_ids = fields.One2many('fabrication', 'bp_sale_order_line_id', string="Fabrication(s)", readonly=True)
    
    bp_total_cost_material = fields.Float(string="Coût total fournitures", store=True, compute="_compute_total_cost_material", help="Coût total fournitures")
    bp_total_hours_fab = fields.Float(string="Nbr heures", store=True, compute="_compute_total_hours_fab", help="Total d'heures")
    bp_total_cost_mo = fields.Float(string="Coût MO", store=True, compute="_compute_total_cost_mo")
    
    @api.depends('bp_material_line_ids.bp_cost')
    def _compute_total_cost_material(self):
        for record in self:
            sum_furniture = sum(record.bp_material_line_ids.mapped('bp_cost'))
            record.bp_total_cost_material = sum_furniture
    
    @api.depends('bp_fab_ids.bp_duration')
    def _compute_total_hours_fab(self):
        for record in self:
            sum_hours = sum(record.bp_fab_ids.mapped('bp_duration'))
            record.bp_total_hours_fab = sum_hours
            
    @api.depends('bp_total_hours_fab','order_id.bp_hourly_rate')
    def _compute_total_cost_mo(self):
        for record in self:
            record.bp_total_cost_mo = record.bp_total_hours_fab * record.order_id.bp_hourly_rate
    
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
        # list_description = dict(self.env['account.analytic.line']._fields['bp_list_desc'].selection)
        # manufacturing_tasks = [{'name': element} for element in list_description.values()]

        list_description_product_tag = self.env['timesheet.description'].search([('bp_product_ids','in',[self.product_id.id])])
        if list_description_product_tag:
            list_description = list_description_product_tag
        else:
            list_description = self.env['timesheet.description'].search([('bp_is_default','=',True)])
        manufacturing_tasks = [{'name': element.name, 'bp_unit_duration': element.bp_default_time, 'bp_timesheet_description_id': element.id} for element in list_description]
        return manufacturing_tasks
    
    def action_open_fabrication_line(self):
        action = { 
                    'type': 'ir.actions.act_window', 
                    'name': 'Lignes de fabrication', 
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'target': 'new',
                    'res_model': 'fabrication',
                    'domain': [('bp_sale_order_line_id', '=', self.id)]
                 }
        return action
        
    def action_open_material_line(self):
        view_id = self.env.ref('ouvrage_line.material_line_tree_bp').id
        action = { 
                    'type': 'ir.actions.act_window', 
                    'name': 'Lignes de matériel', 
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'views': [[view_id, 'tree']],
                    'target': 'new',
                    'res_model': 'material.line',
                    'domain': [('bp_sale_order_line_id', '=', self.id)]
                 }
        return action
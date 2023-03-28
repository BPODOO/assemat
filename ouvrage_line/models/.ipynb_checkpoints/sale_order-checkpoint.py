# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _default_coeff_fab(self):
        return self.env['ir.config_parameter'].sudo().get_param('ouvrage.BP_COEFF_FAB')
    
    @api.model
    def _default_coeff_material(self):
        return self.env['ir.config_parameter'].sudo().get_param('ouvrage.BP_COEFF_MATERIAL')
    
    @api.model
    def _default_hourly_rate(self):
        return self.env['ir.config_parameter'].sudo().get_param('ouvrage.BP_HOURLY_RATE')
    
    bp_coefficient_material = fields.Float(string="Coefficient matériel", default=_default_coeff_material, copy=True)
    bp_coefficient_manufacturing = fields.Float(string="Coefficient fabrication", default=_default_coeff_fab, copy=True)
    bp_hourly_rate = fields.Float(string="Taux horaire", default=_default_hourly_rate, copy=True)
    bp_task_to_create = fields.Boolean(compute='_compute_task_to_create', store=True)
    
    bp_is_copy = fields.Boolean(default=False)

    #OVERIDE
    def copy_data(self, default=None):
        res = super(SaleOrder, self).copy_data(default)
        res[0]['bp_is_copy'] = True
        return res
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrder, self).create(vals_list)
        if(vals_list[0].get('bp_is_copy')):
            dict_lines = dict(zip(self.order_line, res.order_line))
            
            for k, v in dict_lines.items():
                if(k.bp_ouvrage_line):
                    default_update = {
                                        'bp_sale_order_id': res.id,
                                        'bp_sale_order_line_id': v.id,
                                     }
    
                    new_ouvrage = k.bp_ouvrage_line.copy()
                    new_ouvrage.update(default_update)
                    default_update['bp_ouvrage_line_id'] = new_ouvrage.id
                
                    for line in k.bp_ouvrage_line.bp_material_line_ids:
                        new_material = line.copy()
                        new_material.update(default_update)
                    for line in k.bp_ouvrage_line.bp_fabrication_ids:
                        new_fab = line.copy()
                        new_fab.update(default_update)
        return res
    
    #Regarde sur les lignes si une des lignes n'a pas de tâche
    @api.depends('order_line.bp_task_id')
    def _compute_task_to_create(self):
        self.bp_task_to_create = False if len(self.order_line) <= 0 else True if not all(line.bp_task_id for line in self.order_line) else False
    
    def action_create_task(self):
        lines = list(filter(lambda line: not line.bp_task_id, self.order_line))
        if not self.bp_worksite:
            raise ValidationError("Aucun chantier n'est défini !")
        for line in lines:
            task = self.env['project.task'].create({
                                                     'name': f'{line.name} - {self.name}', 
                                                     'project_id': self.bp_worksite.id, 
                                                     'partner_id': self.partner_id.id, 
                                                     'bp_sale_line_origin_task': line.id
                                                  })
            line.update({
                            'bp_task_id': task.id,
                       })
    
    def action_recalculation(self):
        #Application du nouveau taux horaire
        fabrications = self.env['fabrication'].search([('bp_sale_order_id','=',self.id)])
        fabrications._compute_cost()
        #Application des nouveaux coeffs
        ouvrage_lines = self.env['ouvrage.line'].search([('bp_sale_order_id','=',self.id)])
        ouvrage_lines.update({
            'bp_coefficient_material': self.bp_coefficient_material,
            'bp_coefficient_manufacturing': self.bp_coefficient_manufacturing,
        })
        ouvrage_lines._compute_selling_price()
        ouvrage_lines._compute_cost_price()
        #Sauvegarde du prix pour la ligne de vente
        for line in ouvrage_lines: line._save_price()
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
    
    bp_coefficient_material = fields.Float(string="Coefficient matériel", default=_default_coeff_material, copy=False)
    bp_coefficient_manufacturing = fields.Float(string="Coefficient fabrication", default=_default_coeff_fab, copy=False)
    bp_hourly_rate = fields.Float(string="Taux horaire", default=_default_hourly_rate, copy=False)
    bp_task_to_create = fields.Boolean(compute='_compute_task_to_create', store=True)
    
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
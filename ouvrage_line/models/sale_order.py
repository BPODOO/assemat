# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    bp_coefficient_material = fields.Float(string="Coefficient matériel", copy=True)
    bp_coefficient_manufacturing = fields.Float(string="Coefficient fabrication", copy=True)
    bp_hourly_rate = fields.Float(string="Taux horaire", copy=True)
    bp_task_to_create = fields.Boolean(compute='_compute_task_to_create', store=True)
    
    #Regarde sur les lignes si une des lignes n'a pas de tâche
    @api.depends('order_line.bp_task_id')
    def _compute_task_to_create(self):
        _logger.info(self.order_line)
        _logger.info(len(self.order_line))

        self.bp_task_to_create = False if len(self.order_line) <= 0 else True if all(not line.bp_task_id for line in self.order_line) else False
    
    
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
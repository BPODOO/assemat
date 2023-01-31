# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    bp_coefficient_material = fields.Float(string="Coefficient matériel", copy=True)
    bp_coefficient_manufacturing = fields.Float(string="Coefficient fabrication", copy=True)
    bp_hourly_rate = fields.Float(string="Taux horaire", copy=True)
    bp_task_to_create = fields.Boolean(compute='_compute_task_to_create')
    
    @api.depends('order_line')
    def _compute_task_to_create(self):
        if all(not line.bp_active_task for line in self.order_line):
            self.bp_task_to_create = True
        
    def action_create_task(self):
        lines = list(filter(lambda line: not line.bp_active_task, self.order_line))
        _logger.info(lines)
        for line in lines:
            self.env['project.task'].create({'name': "TEST" + line.id})
            line.update({
                            'bp_active_task': True,
                       })
        # for line in self.order_line:
        #     _logger.info(line)
        #     _logger.info(line.bp_active_task)
            # self.env['project.task'].create({'name': "TEST" + line.id})
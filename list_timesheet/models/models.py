# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    bp_timesheet_description_id = fields.Many2one('timesheet.description', string="Type de travaux", copy=False)
    
    @api.onchange('bp_timesheet_description_id')
    def _onchange_timesheet_description(self):
        for record in self:
            record.name = record.bp_timesheet_description_id.name
            
    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountAnalyticLine, self).create(vals_list)
        if res.bp_timesheet_description_id.id == False:
            res.bp_timesheet_description_id = self.bp_timesheet_description_id
        return res
    
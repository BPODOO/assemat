# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    bp_timesheet_description_id = fields.Many2one('timesheet.description', string="Type de travaux", copy=False)

    @api.onchange('bp_timesheet_description_id')
    def _onchange_timesheet_description(self):
        for record in self:
            record.name = record.bp_timesheet_description_id.name
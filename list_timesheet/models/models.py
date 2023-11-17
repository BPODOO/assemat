# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _domain_project_id(self):
        if self.env.user.id == 8:
            domain = [('allow_timesheets', '=', True),("stage_id", "in", [5,6,8])]
        else:
            domain = [('allow_timesheets', '=', True)]
        if not self.user_has_groups('hr_timesheet.group_timesheet_manager'):
            return expression.AND([domain,
                ['|', ('privacy_visibility', '!=', 'followers'), ('message_partner_ids', 'in', [self.env.user.partner_id.id])]
            ])
        return domain
    
    bp_timesheet_description_id = fields.Many2one('timesheet.description', string="Type de travaux", copy=False)
    project_id = fields.Many2one(
        'project.project', 'Project', domain=_domain_project_id, index=True,
        compute='_compute_project_id', store=True, readonly=False)
    
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

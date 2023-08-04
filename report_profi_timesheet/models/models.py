# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'project.project'
    
    def action_print_report_renta_timesheet(self):
        
        url = '/web/binary/print_report_renta_timesheet?project_ids=%s' % self.ids
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

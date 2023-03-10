from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ReportWorksiteSheet(models.AbstractModel):
    _name = "report.worksite_sheet.report_worksite_sheet_document"
    _description = "Fiche de chantier"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):
        
        _logger.info(data['data'])
        
        return {
            'doc_ids' : docids,
            # 'docs': docs,
            'sale_lines': self.env['sale.order.line'].browse(data['data']['sale_line_ids']),
            'ouvrage_lines': self.env['ouvrage.line'].browse(data['data']['ouvrage_line_ids']),
            'project_id': self.env['project.project'].browse(data['data']['project_id']),
        }
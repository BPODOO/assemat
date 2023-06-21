from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ReportTimesheet(models.AbstractModel):
    _name = "report.hr_timesheet.report_timesheet"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):

        # Récupère les ids des enregistrements concernés par le rapport
        obj = self.env['account.analytic.line'].browse(docids)

        # Trie les lignes selon leur tâches et leur type de travaux
        lines_ordered = self.env['account.analytic.line'].search([['id','in',docids]],order="task_id desc, name asc") 
        
        return {
            'docs': obj, 
            'lines_ordered': lines_ordered,
        }

class ReportTimesheet(models.AbstractModel):
    _name = "report.hr_timesheet.report_timesheet_project"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):

        def _get_timesheet_line(project_id):
            lines_ordered = self.env['account.analytic.line'].search([('project_id','=',project_id)],order="task_id desc, name asc") 
            return lines_ordered
              
        return {
            'docs': self.env['project.project'].browse(docids),
            '_get_timesheet_line': _get_timesheet_line
        }


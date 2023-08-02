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
        lines_ordered_grouped = list()
           
        #Groupe par employé dans chaque section
        current_time = "init"
        current_line = {"task_id":"", "worktype":""}
        for line in lines_ordered:
            #Si on change de section
            if line.task_id.name != current_line["task_id"] or line.name != current_line["worktype"]:
                if current_time != "init":
                    current_line["worktime"] = current_time
                    lines_ordered_grouped.append(current_line)

                # On crée la nouvelle ligne
                current_line = {
                    "employee":line.user_id.partner_id.name if line.user_id.partner_id.name else line.employee_id,
                    "project_id": line.project_id.sudo().name,
                    "task_id": line.task_id.name,
                    "worktype": line.name,
                    }
                current_time = line.unit_amount
            else:
                current_time += line.unit_amount
                
        current_line["worktime"] = current_time            
        lines_ordered_grouped.append(current_line)
        
        return {
            'docs': obj, 
            'lines_ordered': lines_ordered_grouped,
        }

class ReportTimesheet(models.AbstractModel):
    _name = "report.hr_timesheet.report_timesheet_project"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):

        def _get_timesheet_line(project_id):
            # Trie les lignes selon leur tâches et leur type de travaux
            lines_ordered = self.env['account.analytic.line'].search([('project_id','=',project_id)],order="task_id desc, name asc") 
            lines_ordered_grouped = list()
           
            #Groupe par employé dans chaque section
            current_time = "init"
            current_line = {"task_id":"", "worktype": "", "employee":""}
            for line in lines_ordered:
                #Si on change de section
                line_name = line.user_id.partner_id.name if line.user_id.partner_id.name else line.employee_id.name
                if line.task_id.name != current_line["task_id"] or line.name != current_line["worktype"] or line_name != current_line["employee"]:
                    if current_time != "init":
                        current_line["worktime"] = current_time
                        lines_ordered_grouped.append(current_line)

                    # On crée la nouvelle ligne
                    current_line = {
                        "employee": line_name,
                        "project_id": line.project_id.sudo().name,
                        "task_id": line.task_id.name,
                        "worktype": line.name,
                        }
                    current_time = line.unit_amount
                else:
                    current_time += line.unit_amount
                    
            current_line["worktime"] = current_time            
            lines_ordered_grouped.append(current_line)

            return lines_ordered_grouped
              
        return {
            'docs': self.env['project.project'].browse(docids),
            '_get_timesheet_line': _get_timesheet_line,
            'is_uom_day': self.env['project.project'].browse(docids).timesheet_ids._is_timesheet_encode_uom_day()
        }


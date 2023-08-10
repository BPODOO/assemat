from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ReportTimesheet(models.AbstractModel):
    _name = "report.hr_timesheet.report_timesheet_project"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):

        def _get_timesheet_line(project_id):
            # Trie les lignes selon leur tâches et leur type de travaux
            lines_ordered = self.env['account.analytic.line'].search([('project_id','=',project_id)],order="task_id desc, name asc,employee_id asc") 
            lines_ordered_grouped = list()
           
            #Groupe par employé dans chaque section
            current_time = "init"
            current_line = {"task_id":"", "worktype": "", "employee":""}
            for line in lines_ordered:
                line_user_name = line.user_id.partner_id.name if line.user_id.partner_id.name else line.employee_id.name

                #Si on change de section, de tâches ou d'employé
                if line.task_id.name != current_line["task_id"] or line.name != current_line["worktype"] or line_user_name != current_line["employee"]:
                    if current_time != "init":
                        current_line["worktime"] = current_time
                        lines_ordered_grouped.append({"display_type":"line", "data":current_line}) # On ajoute la ligne à la liste des lignes
                        
                    # On crée ensuite les lignes d'entêtes de tâches et type de travaux si nécéssaire
                    if line.task_id.name != current_line["task_id"]:
                        worktime_task = sum(lines_ordered.filtered(lambda x: x.task_id == line.task_id).mapped('unit_amount'))
                        lines_ordered_grouped.append({"display_type":"task", "data":{"task":line.task_id.name, "worktime":worktime_task}})

                        worktime_worktype = sum(lines_ordered.filtered(lambda x: x.task_id == line.task_id and x.name == line.name).mapped('unit_amount'))
                        lines_ordered_grouped.append({"display_type":"worktype", "data":{"worktype":line.name, "worktime":worktime_worktype}})
                        
                    elif line.name != current_line["worktype"]:
                        worktime_worktype = sum(lines_ordered.filtered(lambda x: x.task_id == line.task_id and x.name == line.name).mapped('unit_amount'))
                        lines_ordered_grouped.append({"display_type":"worktype", "data":{"worktype":line.name, "worktime":worktime_worktype}})
                        
                    

                    # On crée la nouvelle ligne
                    current_line = {
                        "employee": line_user_name,
                        "project_id": line.project_id.sudo().name,
                        "task_id": line.task_id.name,
                        "worktype": line.name,
                        }
                    current_time = line.unit_amount
                else: # Sinon, on ajoute le temps à la ligne
                    current_time += line.unit_amount
                    
            current_line["worktime"] = current_time            
            lines_ordered_grouped.append({"display_type":"line", "data":current_line})

            return lines_ordered_grouped
              
        return {
            'docs': self.env['project.project'].browse(docids),
            '_get_timesheet_line': _get_timesheet_line,
            'is_uom_day': self.env['project.project'].browse(docids).timesheet_ids._is_timesheet_encode_uom_day()
        }


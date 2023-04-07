from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import datetime
import time
import pytz

class ReportWorksiteSheet(models.AbstractModel):
    _name = "report.worksite_sheet.report_worksite_sheet_document"
    _description = "Fiche de chantier"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):
        
        objet_section = data['data']['objet_section']
        fabrication_lines = self.env['fabrication'].search([['bp_sale_order_line_id', 'in', data['data']['sale_line_ids']]])
        materials_lines = self.env['material.line'].search([['bp_sale_order_line_id', 'in', data['data']['sale_line_ids']]])
        materials_lines_group = self.group_materials_by_sale_order_line(materials_lines,fabrication_lines)
        _logger.info(materials_lines_group)
        materials_lines_group = self.group_ouvrage_line_by_page(materials_lines_group)
        _logger.info(materials_lines_group)
        return {
            'doc_ids' : docids,
            # 'docs': docs,
            'date_now': datetime.datetime.now().astimezone(pytz.timezone('Europe/Berlin')).strftime("%d-%m-%Y %H:%M:%S"),
            'objet_section': objet_section,
            'sale_lines': self.env['sale.order.line'].browse(data['data']['sale_line_ids']),
            'materials_lines': materials_lines_group,
            'ouvrage_lines': self.env['ouvrage.line'].browse(data['data']['ouvrage_line_ids']),
            'project_id': self.env['project.project'].browse(data['data']['project_id']),
        }
    
    def group_materials_by_sale_order_line(self,records,fabrications):
        materials_group = {}
        # fabrication_totals = self._time_total_by_sale_order_line(fabrications)
        for record in records:
            key = record.bp_sale_order_line_id.name +'_'+ str(record.bp_sale_order_line_id.id)
            if key in materials_group.keys():
                # materials_group[key]['qty_total'] += record.bp_qty
                materials_group[key]['lines'].append(record)
            else:
                materials_group[key] = {'lines': [record]}
                # materials_group[key] = {'qty_total': record.bp_qty, 'lines': [record]}
        # for fab_key in fabrication_totals:
        #     materials_group[fab_key]['time_total'] = fabrication_totals[fab_key]['time_total']
        return materials_group
    
    def group_ouvrage_line_by_page(self, ouvrage_lines):
        page_group = {'P_left':[], 'P_right':[], 'number_page':1}
        limit = 20
        swap = True
        list_page = []
        
        for ouvrage in ouvrage_lines:
            _logger.info(ouvrage)
            _logger.info(len(ouvrage_lines[ouvrage]['lines']))
            count_material_lines = len(ouvrage_lines[ouvrage]['lines'])
            limit = limit - count_material_lines
            _logger.info(limit)
            if limit < 0:
                if swap:
                    page_group['P_left'].append(list_page)
                    list_page = []
                    list_page.append({ouvrage:{'lines':ouvrage_lines[ouvrage]['lines']}})
                else:
                    page_group['P_right'].append(list_page)
                    list_page = []
                    list_page.append({ouvrage:{'lines':ouvrage_lines[ouvrage]['lines']}})
                    page_group['number_page'] += 1
                swap = not swap
                limit = 20 - count_material_lines
            else:
                list_page.append({ouvrage:{'lines':ouvrage_lines[ouvrage]['lines']}})
        if swap:
            page_group['P_left'].append(list_page)
        else:
            page_group['P_right'].append(list_page)
        return page_group
            
    # def _time_total_by_sale_order_line(self,records):
    #     fabrication_group = {}
    #     for record in records:
    #         key = record.bp_sale_order_line_id.name
    #         fabrication_line = {'time_total': 0}
    #         if key in fabrication_group.keys():
    #             fabrication_group[key]['time_total'] += record.bp_duration
    #         else:
    #             fabrication_group[key] = {'time_total': record.bp_duration}
    #     return fabrication_group
        
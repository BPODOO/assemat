# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'
    
    def action_view_project_form(self):
        action = self.env['ir.actions.actions']._for_xml_id('project_redirection.action_view_project_form_bp')
        action['res_id'] = self.id
        return action
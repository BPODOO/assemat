# -*- coding: utf-8 -*-

from odoo import models, fields, api

class projet_creer_redirection(models.Model):
    _inherit="project.project"
    
    def action_view_project_form(self):
        return {
                    'name': self.name,
                    'view_mode': 'form',
                    'res_model': 'project.project',
                    'type': 'ir.actions.act_window',
                    'res_id': self.id,
                }

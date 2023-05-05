# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    bp_timesheet_description_id = fields.Many2one('timesheet.description', string="Type de travaux", copy=False)
    
    bp_list_desc = fields.Selection([("prise de cote", "Prise de cote"),('etude projet', 'Etude projet'),('bureau dessin', 'Bureau dessin'),('approvisionnement matériel', 'Approvisionnement matériel'),('débit scie', 'Débit scie'),('echantage', 'Echantage'),("centre d'usinage", "Centre d'usinage"),("rabotage degauchissage", "Rabotage / Dégauchissage"),("toupillage", "Toupillage"),("placage stratifié en presse", "Placage stratifié en presse"),("placage stratifié pistolable", "Placage stratifié pistolable"),("ponçage et finitions", "Ponçage et finitions"),("vernissage et peinture", "Vernissage et peinture"),("montage en atelier", "Montage en atelier"),("tiroirs", "Tiroirs"),("emballage", "Emballage"),("fabrication palette de transport", "Fabrication palette de transport"),("chargement", "Chargement"),("nettoyage atelier", "Nettoyage atelier"),("évacuation des copeaux", "Évacuation des copeaux"),("entretien atelier", "Entretien atelier"),("trajet","Trajet"),("pose","Pose")], string="Type de travaux")
  
    @api.onchange('bp_list_desc')
    def complete_description(self):
        for record in self:
            record['name'] = record.bp_list_desc

    @api.onchange('bp_timesheet_description_id')
    def _onchange_timesheet_description(self):
        for record in self:
            record.name = record.bp_timesheet_description_id.name
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    bp_list_desc = fields.Selection([('bureau dessin', 'Bureau dessin'),('approvisionnement matériel', 'Approvisionnement matériel'),('débit scie', 'Débit scie'),('echantage', 'Echantage'),("centre d'usinage", "Centre d'usinage"),("montage en atelier", "Montage en atelier"),("placage stratifié en presse", "Placage stratifié en presse"),("placage stratifié pistolable", "Placage stratifié pistolable"),("ponçage et finitions", "Ponçage et finitions"),("vernissage et peinture", "Vernissage et peinture"),("vernissage et peinture", "Vernissage et peinture"),("emballage", "Emballage"),("fabrication palette de transport", "Fabrication palette de transport"),("chargement", "Chargement"),("nettoyage atelier", "Nettoyage atelier"),("évacuation des copeaux", "Évacuation des copeaux"),("entretien atelier", "Entretien atelier"),("prise de cote", "Prise de cote"),("pose","Pose"),("trajet","Trajet")])

    
    @api.onchange('bp_list_desc')
    def complete_description(self):
        for record in self:
            record['name'] = record.bp_list_desc
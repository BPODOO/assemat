# -*- coding: utf-8 -*-
{
    'name': "Rapport Feuilles de Temps ",

    'summary': """
        Modification du rapport de feuille de temps""",

    'description': """
        Ajout d'un regroupement par tâche puis par type de travaux
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_timesheet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report_timesheet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

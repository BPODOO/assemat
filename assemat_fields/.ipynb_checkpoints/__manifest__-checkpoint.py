# -*- coding: utf-8 -*-
{
    'name': "Assemat Fields",

    'summary': """
        Met à disposition des champs essentiels au flux de l'entreprise Assemat""",

    'description': """
        Affiche des champs et des vues essentielles pour le fonctionnement Assemat.
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',
    #Copyright 2023 BeProject

    # any module necessary for this one to work correctly
    'depends': ['base','sale','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/views_project.xml',
    ],
}

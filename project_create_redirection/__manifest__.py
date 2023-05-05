# -*- coding: utf-8 -*-
{
    'name': "Redirection vers projet",

    'summary': """
        Modification de l'action de redirection lors de la création d'un projet.
    """,

    'description': """
        Lors de la création d'un projet l'utilisateur apparait directement sur la vue Form du projet.
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}

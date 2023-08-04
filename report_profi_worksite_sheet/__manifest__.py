# -*- coding: utf-8 -*-
{
    'name': "Rapport Fusion Rentabilité détaillé et Feuilles de temps",

    'summary': """
        Fusion rapport Rentabilité détaillé et Feuilles de temps""",

    'description': """
        Impression depuis le menu Action, cette action imprime sur un seul PDF le rapport
        Rentabilité détaillé et Feuilles de temps
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",
    'license': "GPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}

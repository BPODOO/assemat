# -*- coding: utf-8 -*-
{
    'name': "Rapport Rentabilité détaillé",

    'summary': """
        Rapport rentabilité sur les lignes ventes""",

    'description': """
        Rapport rentabilité des fournitures trier par section et détaillées
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

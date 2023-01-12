# -*- coding: utf-8 -*-
{
    'name': "Ouvrage",

    'summary': """
        Permet le calcul d'une ligne de vente""",

    'description': """
        Propose une interface de calcul pour le prix d'une prestation (ligne de vente) en fonction de plusieurs paramètres.
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license' 'LGPL-3',
    
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}

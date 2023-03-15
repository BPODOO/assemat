# -*- coding: utf-8 -*-
{
    'name': "Redirection vers projet",

    'summary': """
        Module permettant d'afficher le formlaire d'un projet lors du click sur sa kanban box""",

    'description': """
        Module permettant de rediriger la vue kanban box vers la vue formulaire d'un projet
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",
    # Copyright 2023 BeProject
    'license': 'LGPL-3',

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/views_project_kanban.xml',
    ],
}

# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectCreateRedirection(http.Controller):
#     @http.route('/project_create_redirection/project_create_redirection', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_create_redirection/project_create_redirection/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_create_redirection.listing', {
#             'root': '/project_create_redirection/project_create_redirection',
#             'objects': http.request.env['project_create_redirection.project_create_redirection'].search([]),
#         })

#     @http.route('/project_create_redirection/project_create_redirection/objects/<model("project_create_redirection.project_create_redirection"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_create_redirection.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectRedirection(http.Controller):
#     @http.route('/project_redirection/project_redirection', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_redirection/project_redirection/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_redirection.listing', {
#             'root': '/project_redirection/project_redirection',
#             'objects': http.request.env['project_redirection.project_redirection'].search([]),
#         })

#     @http.route('/project_redirection/project_redirection/objects/<model("project_redirection.project_redirection"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_redirection.object', {
#             'object': obj
#         })

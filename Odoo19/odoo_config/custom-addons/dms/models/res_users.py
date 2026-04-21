from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    dms_role = fields.Selection([
        ('none', 'None'),
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Administrator'),
    ], string='DMS Role', default='none', compute='_compute_dms_role', inverse='_inverse_dms_role')

    def _compute_dms_role(self):
        for user in self:
            if user.has_group('dms.group_dms_manager'):
                user.dms_role = 'admin'
            elif user.has_group('dms.group_dms_user'):
                user.dms_role = 'editor'
            elif user.has_group('dms.group_dms_viewer'):
                user.dms_role = 'viewer'
            else:
                user.dms_role = 'none'

    def _inverse_dms_role(self):
        viewer = self.env.ref('dms.group_dms_viewer')
        editor = self.env.ref('dms.group_dms_user')
        admin = self.env.ref('dms.group_dms_manager')
        groups = viewer | editor | admin
        for user in self:
            group_to_add = self.env['res.groups']
            if user.dms_role == 'viewer':
                group_to_add = viewer
            elif user.dms_role == 'editor':
                group_to_add = editor
            elif user.dms_role == 'admin':
                group_to_add = admin
            super(ResUsers, user).write({'groups_id': [(5, 0, 0)] + ([(4, group_to_add.id)] if group_to_add else [])})

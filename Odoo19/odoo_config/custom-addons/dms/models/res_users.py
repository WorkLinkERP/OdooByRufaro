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
        all_dms_groups = [viewer, editor, admin]

        role_map = {
            'viewer': viewer,
            'editor': editor,
            'admin': admin,
        }

        for user in self:
            target_group = role_map.get(user.dms_role)
            for group in all_dms_groups:
                if group == target_group:
                    group.sudo().write({'users': [(4, user.id)]})
                else:
                    group.sudo().write({'users': [(3, user.id)]})

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
        all_group_ids = [viewer.id, editor.id, admin.id]

        role_map = {
            'viewer': viewer.id,
            'editor': editor.id,
            'admin': admin.id,
        }

        for user in self:
            target_group_id = role_map.get(user.dms_role)
            self.env.cr.execute(
                "DELETE FROM res_groups_users_rel WHERE uid = %s AND gid = ANY(%s)",
                (user.id, all_group_ids)
            )
            if target_group_id:
                self.env.cr.execute(
                    "INSERT INTO res_groups_users_rel (uid, gid) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (user.id, target_group_id)
                )
        self.env['res.users'].invalidate_model(['groups_id'])
        self.env['res.groups'].invalidate_model(['users'])

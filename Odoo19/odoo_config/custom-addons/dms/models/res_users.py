from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    dms_role = fields.Selection([
        ('none', 'None'),
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Administrator'),
    ], string='DMS Role', default='none', compute='_compute_dms_role', readonly=False)

    @api.depends('group_ids')
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

    @api.onchange('dms_role')
    def _onchange_dms_role(self):
        viewer = self.env.ref('dms.group_dms_viewer')
        editor = self.env.ref('dms.group_dms_user')
        admin = self.env.ref('dms.group_dms_manager')
        dms_groups = viewer | editor | admin
        for user in self:
            groups = user.group_ids - dms_groups
            if user.dms_role == 'viewer':
                groups |= viewer
            elif user.dms_role == 'editor':
                groups |= editor
            elif user.dms_role == 'admin':
                groups |= admin
            user.group_ids = groups

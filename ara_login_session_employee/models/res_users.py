from odoo import models, fields, api, http, _
from odoo.http import request

# import logging
# _logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    access_user_employees = fields.Many2many(
        'hr.employee',
        'employee_user_rel',
        'employee_id',
        'related_employee_id',
        string='Employees Access Multi By Session',
        help='Select the "Employee" who is the user of this account that is linked to the User Account'
    )
    activity_session_login_ids = fields.One2many(
        string="Activity Session Login Employee",
        comodel_name="activity.session",
        inverse_name="user_id",
    )

    def open_employee_sessions(self):
        return {
            'name': _(' Employee Access Login By Session'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'list,form',
            'res_model': 'hr.employee',
            'context': {'create': False, 'delete': False},
            'domain': [('id', 'in', self.access_user_employees.ids)],
        }

    def session_logout(self):
        # Clear specific session variables during logout
        session_id = request.session.sid
        session_get = self.env['activity.session'].search([('session_id', '=', session_id)])
        print("HSLLLE", )
        print(session_get)
        request.session.pop('selected_employee', None)

        # Call the original session logout to clear other session data
        return super(ResUsers, self).session_logout()

    def check_selected_employee(self):
        # Check if 'selected_employee' is in the session
        if not request.session.get('selected_employee'):
            # Redirect to the employee selection wizard
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'employee.selection.wizard',
                'view_mode': 'form',
                'target': 'new',
            }
        return None

    @http.route('/web/pre_dispatch', type='json', auth='user')
    def pre_dispatch(self):
        # Check if 'selected_employee' is in the session
        if not request.session.get('selected_employee'):
            # Force user to select an employee
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'employee.selection.wizard',
                'view_mode': 'form',
                'target': 'new',
            }
        return super(ResUsers, self).pre_dispatch()

from odoo import models, fields, api, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError


class EmployeeSelectionWizard(models.TransientModel):
    _name = 'employee.selection.wizard'
    _description = 'Employee Selection Wizard'

    employee_id = fields.Many2one(
        'hr.employee',
        string="Select Employee",
        domain=lambda self: self._get_employee_domain()
    )

    pin = fields.Char(string="Enter PIN", required=True)
    ip_address = fields.Char(
        string="IP Address",
        compute='_get_ip_address'
    )

    def _get_employee_domain(self):
        # Get the currently logged-in user
        user = self.env.user

        # Find the employee record for the current user
        employee = user.access_user_employees

        if employee:
            # Get employees from the user's access_user_employees field
            employee_ids = employee.filtered(
                lambda e: e.pin).ids

        else:
            employee_ids = []

        # Set domain to filter employees based on the access_user_employees field
        return [('id', 'in', employee_ids)]

    def _get_ip_address(self):
        ip = request.httprequest.headers.get(
            'X-Forwarded-For', request.httprequest.remote_addr)
        self.ip_address = ip
    
    def create_session_employee(self):
        user = self.env.user
        user_agent = request.httprequest.headers.get('User-Agent', '')
        session_id = request.session.sid  # <-- Ambil session ID saat ini

        # Simple OS detection
        os = 'Unknown OS'
        browser = 'Unknown Browser'

        if 'Windows' in user_agent:
            os = 'Windows'
        elif 'Macintosh' in user_agent:
            os = 'macOS'
        elif 'Linux' in user_agent:
            os = 'Linux'
        elif 'Android' in user_agent:
            os = 'Android'
        elif 'iPhone' in user_agent:
            os = 'iOS'

        if 'Chrome' in user_agent and 'Safari' in user_agent:
            browser = 'Chrome'
        elif 'Firefox' in user_agent:
            browser = 'Firefox'
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            browser = 'Safari'
        elif 'Edge' in user_agent:
            browser = 'Edge'
        elif 'OPR' in user_agent or 'Opera' in user_agent:
            browser = 'Opera'

        self.env['activity.session'].create({
            'user_id': user.id,
            'employee_id': self.employee_id.id,
            'ip_address': self.ip_address,
            'os_device': os,
            'web_browser': browser,
            'status': 'on',
            'session_id': session_id,  # <-- Simpan session ID di sini
        })


    def _check_ip_indicator(self):
        is_ip = self.employee_id.sudo().ip_address
        if is_ip and is_ip != self.sudo().ip_address:
            raise UserError(_("IP ADDRESS Different with Setup"))

    def action_select(self):
        selected_employee = self.employee_id
        entered_pin = self.pin
        self._check_ip_indicator()

        if selected_employee and selected_employee.pin != entered_pin:
            raise UserError(_("Authentication failed: PIN does not match employee !"))

        if selected_employee:
            request.session['selected_employee'] = selected_employee.name
            request.session['selected_employee_id'] = selected_employee.id
        self.create_session_employee()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

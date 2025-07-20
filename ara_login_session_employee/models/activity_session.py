from odoo import models, fields, api, _, http
from odoo.exceptions import UserError
from odoo.http import request
from odoo.http import Session
import os


class ActivitySession(models.Model):
    _name = 'activity.session'
    _order = 'create_date desc'  # Urutkan dari yang terbaru

    user_id = fields.Many2one(
        'res.users',
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
    )

    ip_address = fields.Char(
        string="Ip Address",
    )

    os_device = fields.Char(
        string="Operating System",
    )

    web_browser = fields.Char(
        string="Web Browser",
    )

    status = fields.Selection(
        selection=[
            ("on", "On"),
            ("off", "Off"),
        ],
        string="Status", store=True
    )
    # pastikan field ini diisi saat login
    session_id = fields.Char("Session ID")

    def force_logout(self):
        """
        Force logout a user by deleting the session file,
        except if it's the current user's own session.
        """
        session_store = http.root.session_store
        current_session_id = http.request.session.sid

        if self.status == 'off':
            raise UserError("Session already logged out.")

        if self.session_id == current_session_id:
            raise UserError("You cannot force logout your own active session.")

        try:
            path = session_store.get_session_filename(self.session_id)
            if os.path.exists(path) and self.status == 'on':
                self.update({'status': 'off'})
                os.remove(path)
                return {"status": "success", "message": f"User with session {self.session_id} logged out."}
            else:
                return {"status": "error", "message": f"Session file not found for session {self.session_id}."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

from odoo import models, api
from odoo.http import request
from werkzeug.local import LocalProxy


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        # Pastikan akses request.session hanya jika memang sedang dalam HTTP request
        employee = False
        if isinstance(request, LocalProxy):
            try:
                employee = request.session.get('selected_employee', False)
            except RuntimeError:
                employee = False

        # Tambahkan info employee jika ada
        if employee and 'body' in values:
            values['body'] = f"{values['body']}\n- {employee}"

        return super(MailMessage, self).create(values)

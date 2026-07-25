from odoo import api, models
from odoo.http import request


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model_create_multi
    def create(self, vals_list):
        employee = False

        try:
            if request and hasattr(request, "session"):
                employee = request.session.get("selected_employee", False)
        except Exception:
            employee = False

        if employee:
            for vals in vals_list:
                if vals.get("body"):
                    vals["body"] = f"{vals['body']}<br/><b>Created by employee : {employee} </b>"

        return super().create(vals_list)
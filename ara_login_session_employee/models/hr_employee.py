from odoo import models, fields
from odoo.http import request


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ip_address = fields.Char(
        string="IP Address",
    )

    def get_ip_address(self):
        ip = request.httprequest.headers.get(
            'X-Forwarded-For', request.httprequest.remote_addr)
        self.update({
            'ip_address': ip
        })

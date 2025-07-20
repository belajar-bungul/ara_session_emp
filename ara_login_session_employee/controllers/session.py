from odoo import http
from odoo.http import request


class Session(http.Controller):

    @http.route('/web/session/logout', type='http', auth='none', readonly=True)
    def logout(self, redirect='/odoo'):
        session_id = request.session.sid
        activity_session = request.env['activity.session'].sudo().search([
            ('session_id', '=', session_id),
            ('status', '=', 'on'),
        ], limit=1)

        if activity_session:
            activity_session.write({'status': 'off'})

        request.session.logout(keep_db=True)
        return request.redirect(redirect, 303)

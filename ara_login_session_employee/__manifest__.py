# -*- coding: utf-8 -*-
{
    'name': 'Employee-Based Session Auth – Login, Track, and Force Logout by Employee',
    'version': '18.0.0.0.0',
    'category': 'Extra Tools',
    'summary': 'Special Feature',
    'description': """Allow a single Odoo user account to serve multiple employees, each with their own tracked login session. Authenticate, monitor, and force logout sessions per employee — perfect for shared accounts with employee-based session control. """,
    'author': 'ARA SOFT',
    'company': '',
    'maintainer': 'ARA SOFT',
    'website': "",
    'depends': ['hr', 'contacts', 'base', 'mail','web'],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/employee.xml",
        "views/login_views.xml",
        "views/res_users_views.xml",
        "wizard/employee_selection_wizard_views.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'ara_login_session_employee/static/src/js/systray_icon.js',
            'ara_login_session_employee/static/src/xml/systray_icon.xml',
            'ara_login_session_employee/static/src/css/custom_modal.css',
        ],
    },
    'images': [
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
    'application': True,
    'price' : 83.23,
    "currency": "USD",
}

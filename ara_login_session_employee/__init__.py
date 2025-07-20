from . import models
from . import wizard
from . import controllers


def post_init_hook(env):
    user_admin = env.ref('base.user_admin', raise_if_not_found=False)
    if user_admin:
        employee = user_admin.employee_id
        if not employee.pin:
            employee.pin = '1234'
        user_admin.access_user_employees = [(4, employee.id)]

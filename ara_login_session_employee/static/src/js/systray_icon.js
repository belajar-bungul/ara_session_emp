/** @odoo-module **/
import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { Component } from "@odoo/owl"

class SystrayIcon extends Component {
    static template = "ara_login_session_employee.SessionSystray"
    setup() {
        super.setup(...arguments)
        this.action = useService("action")
        this.updateSelectedEmployeeStatus()
    }

    updateSelectedEmployeeStatus() {
        // Access the DOM element with ID 'session_employee'
        const sessionEmployeeElement =
            document.getElementById("session_employee")

        // Check if the element exists and retrieve its value
        if (sessionEmployeeElement) {
            const selectedEmployee = sessionEmployeeElement.textContent.trim()
            this.hasSelectedEmployee = selectedEmployee !== "no session"
        } else {
            // Handle the case where the element is not found
            this.hasSelectedEmployee = false
        }
    }

    _openSession() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Start your session",
            res_model: "employee.selection.wizard",
            view_mode: "form",
            views: [[false, "form"]],
            target: "new",
        })
    }
}

export const systrayItem = {
    Component: SystrayIcon,
}

registry
    .category("systray")
    .add("ara_login_session_employee.SessionSystray", systrayItem, {
        sequence: 1,
    })

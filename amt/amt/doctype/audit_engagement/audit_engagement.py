# Copyright (c) 2025, Ashar Shamsudheen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AuditEngagement(Document):

    def validate(self):
        self.update_completion_percentage()

    def update_completion_percentage(self):
        tasks = frappe.get_all(
            "Audit Task",
            filters={"audit_engagement": self.name},
            fields=["docstatus", "weight_"]
        )

        if not tasks:
            self.completion_percentage = 0
            return

        total_completed_weight = sum(
            t.weight_ or 0 for t in tasks if t.docstatus == 1
        )

        self.completion_percentage = min(total_completed_weight, 100)

    def on_submit(self):
        if not self.audit_configuration:
            frappe.throw("Audit Configuration must be set before submission.")

        # Step 1: Validate team has all required roles
        required_roles = {
            "Engagement Partner",
            "Audit Manager",
            "Audit Senior",
            "Audit Staff",
            "Tax Reviewer"
        }

        assigned_roles = {member.role for member in self.team_assignment if member.role}
        missing_roles = required_roles - assigned_roles

        if missing_roles:
            missing_list = ", ".join(missing_roles)
            frappe.throw(f"🚫 Incomplete Team Assignment: Missing role(s): {missing_list}")

        # Step 2: Fetch Audit Stage Configuration
        audit_config = frappe.get_doc("Audit Stage Configuration", self.audit_configuration)

        if not audit_config.audit_tasks_child_table:
            frappe.msgprint("No tasks found in the Audit Configuration.")
            return

        # Step 3: Build Role → User map from team_assignment
        role_to_user = {
            member.role: member.user_id
            for member in self.team_assignment
            if member.role and member.user_id
        }

        # Step 4: Create Audit Tasks and assign
        for task in audit_config.audit_tasks_child_table:
            user_id = role_to_user.get(task.responsible_role)

            audit_task = frappe.new_doc("Audit Task")
            audit_task.audit_engagement = self.name
            audit_task.task_name = task.audit_task
            audit_task.audit_stage = task.audit_stage
            audit_task.description = task.description
            audit_task.critical_path = task.critical_path
            audit_task.weight_ = task.weight
            audit_task.assigned_to = user_id  # ✅ Correctly assigned

            audit_task.insert(ignore_permissions=True)

            if user_id:
                frappe.msgprint(f"✅ Created Task: {audit_task.task_name} → Assigned to: {user_id}")
            else:
                frappe.msgprint(f"⚠️ Created Task: {audit_task.task_name} → No user found for role: {task.responsible_role}")

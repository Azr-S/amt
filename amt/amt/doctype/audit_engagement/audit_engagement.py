# Copyright (c) 2025, Ashar Shamsudheen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AuditEngagement(Document):
    
    def on_submit(self):
        if not self.audit_configuration:
            frappe.throw("Audit Configuration must be set before submission.")
        
        # Fetch the linked Audit Stage Configuration document
        audit_config = frappe.get_doc("Audit Stage Configuration", self.audit_configuration)

        if not hasattr(audit_config, "audit_tasks_child_table") or not audit_config.audit_tasks_child_table:
            frappe.msgprint("No tasks found in the Audit Configuration.")
            return

        for task in audit_config.audit_tasks_child_table:
            audit_task = frappe.new_doc("Audit Task")
            audit_task.audit_engagement = self.name                      # Link to current Audit Engagement
            audit_task.task_name = task.audit_task                       # ✅ Correct field for Audit Task Template
            audit_task.audit_stage = task.audit_stage
            audit_task.description = task.description
            audit_task.responsible_person = task.responsible_person
            audit_task.critical_path = task.critical_path

            audit_task.insert(ignore_permissions=True)
            frappe.msgprint(f"Created Audit Task: {audit_task.name}")

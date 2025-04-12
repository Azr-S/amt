# Copyright (c) 2025, Ashar Shamsudheen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AuditTask(Document):

    def validate(self):
        # Sync workflow_state to approval_level_for_kanban before saving
        if self.approval_level_for_kanban != self.workflow_state:
            self.approval_level_for_kanban = self.workflow_state

    def on_update(self):
        # Will be triggered on every save / state transition
        if self.audit_engagement and self.docstatus == 1:
            engagement = frappe.get_doc("Audit Engagement", self.audit_engagement)
            engagement.update_completion_percentage()
            engagement.save(ignore_permissions=True)
            frappe.msgprint(f"🔁 Updated completion percentage for {engagement.name}")

import frappe
from frappe.model.document import Document

class AuditStageConfiguration(Document):

    def on_submit(self):
        self.validate_total_weight()

    def validate_total_weight(self):
        total_weight = 0.0

        for task in self.audit_tasks_child_table:
            if task.weight:
                total_weight += float(task.weight)

        if total_weight != 100.0:
    	    frappe.throw(f"Total weight of all tasks not equal to 100% (currently {total_weight:.2f}%)")

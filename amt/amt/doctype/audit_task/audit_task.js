// Copyright (c) 2025, Ashar Shamsudheen and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Audit Task", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Audit Attachment', {
    description_or_findings: function(frm, cdt, cdn) {
        // Refresh the grid to force the row to "materialize"
        frm.fields_dict["table_bvoc"].grid.refresh();

        // Optional feedback to user
        frappe.show_alert("Row saved. You can now use the Attach Files.");
    }
});

frappe.ui.form.on('Audit Task', {
    onload: function(frm) {
        frm.fields_dict["table_bvoc"].grid.on('grid-render', function(grid) {
            grid.grid_rows.forEach(row => {
                if (!row.doc.description_or_findings) {
                    $(row.wrapper).find('[data-fieldname="attach_doc"] .attach-btn').hide();
                }
            });
        });
    }
});

//save audit task when audit_engagement field is updated
frappe.ui.form.on('Audit Task', {
    audit_engagement: function(frm) {
        frm.save();
    }
});
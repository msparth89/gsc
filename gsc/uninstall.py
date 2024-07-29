# # gsc/uninstall.py

# import frappe

# def remove_custom_fields():
#     # List of custom fields to be removed
#     custom_fields_to_remove = [
#         {'dt': 'User', 'fieldname': 'vpa_id'},
#         {'dt': 'User', 'fieldname': 'country_code'},
#         {'dt': 'Sales Partner', 'fieldname': 'vpa_id'},
#         {'dt': 'Sales Partner', 'fieldname': 'country_code'},
#         {'dt': 'Sales Partner', 'fieldname': 'mobile_no'},
#         {'dt': 'Sales Person', 'fieldname': 'vpa_id'},
#         {'dt': 'Sales Person', 'fieldname': 'country_code'},
#         {'dt': 'Sales Person', 'fieldname': 'country_code'},
#     ]

#     for field in custom_fields_to_remove:
#         if frappe.db.exists('Custom Field', {'dt': field['dt'], 'fieldname': field['fieldname']}):
#             frappe.db.sql("""DELETE FROM `tabCustom Field` WHERE dt = %s AND fieldname = %s""", (field['dt'], field['fieldname']))
#             frappe.db.commit()
#             frappe.msgprint(f"Deleted custom field {field['fieldname']} from {field['dt']}")

# def remove_role_profile():
#     role_profile_name = 'io'
#     if frappe.db.exists('Role Profile', role_profile_name):
#         frappe.db.sql("""DELETE FROM `tabRole Profile` WHERE role_profile_name = %s""", (role_profile_name,))
#         frappe.db.commit()
#         frappe.msgprint(f"Deleted role profile {role_profile_name}")

# def remove_item_group():
#     item_group_name = 'Exchange'
#     if frappe.db.exists('Item Group', item_group_name):
#         frappe.db.sql("""DELETE FROM `tabItem Group` WHERE item_group_name = %s""", (item_group_name,))
#         frappe.db.commit()
#         frappe.msgprint(f"Deleted item group {item_group_name}")

# def after_uninstall():
#     remove_custom_fields()
#     remove_role_profile()
#     remove_item_group()
#     frappe.msgprint("gsc app has been uninstalled and all custom fields and records have been removed.")


# gsc/uninstall.py

import frappe

def before_uninstall():
    delete_custom_fields()
    delete_role_profile()
    delete_item_group()
    delete_commission_rate_field()


def delete_custom_fields():
    custom_fields = [
        {'dt': 'User', 'fieldname': 'vpa_id'},
        {'dt': 'User', 'fieldname': 'country_code'},
        {'dt': 'Sales Partner', 'fieldname': 'vpa_id'},
        {'dt': 'Sales Partner', 'fieldname': 'country_code'},
        {'dt': 'Sales Partner', 'fieldname': 'mobile_no'},
        {'dt': 'Sales Person', 'fieldname': 'vpa_id'},
        {'dt': 'Sales Person', 'fieldname': 'country_code'},
        {'dt': 'Sales Person', 'fieldname': 'country_code'},
    ]

    for field in custom_fields:
        delete_custom_field(field['dt'], field['fieldname'])

def delete_custom_field(doctype, fieldname):
    custom_field_name = frappe.db.exists('Custom Field', {'dt': doctype, 'fieldname': fieldname})
    if custom_field_name:
        frappe.delete_doc('Custom Field', custom_field_name)
        frappe.db.commit()

def delete_role_profile():
    role_profile_name = frappe.db.exists('Role Profile', {'role_profile': 'io'})
    if role_profile_name:
        frappe.delete_doc('Role Profile', role_profile_name)
        frappe.db.commit()

def delete_item_group():
    item_group_name = frappe.db.exists('Item Group', {'item_group_name': 'Exchange'})
    if item_group_name:
        frappe.delete_doc('Item Group', item_group_name)
        frappe.db.commit()

def delete_commission_rate_field():
    custom_field_name = frappe.db.exists('Custom Field', {'dt': 'Item', 'fieldname': 'commission_rate'})
    if custom_field_name:
        frappe.delete_doc('Custom Field', custom_field_name)
        frappe.db.commit()
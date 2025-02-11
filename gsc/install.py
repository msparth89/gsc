# asiatechgsc/install.py

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def after_install():
    add_custom_fields()
    add_role_profile()
    add_item_group()
    create_commission_rate_field()
    change_referral_code_length()

def add_custom_fields():
    custom_fields = {
        "User": [
            {
                "fieldname": "vpa_id",
                "label": "VPA ID",
                "fieldtype": "Data",
                "insert_after": "email",
                "read_only": 0
            },
            {
                "fieldname": "country_code",
                "label": "Country Code",
                "fieldtype": "Data",
                "insert_after": "mobile_no",
                "read_only": 0
            }
        ],
        "Sales Partner": [
            {
                "fieldname": "vpa_id",
                "label": "VPA ID",
                "fieldtype": "Data",
                "insert_after": "commission_rate",
                "read_only": 0
            },
            {
                "fieldname": "country_code",
                "label": "Country Code",
                "fieldtype": "Data",
                "insert_after": "vpa_id",
                "read_only": 0
            },
            {
                "fieldname": "mobile_no",
                "label": "Mobile No",
                "fieldtype": "Data",
                "insert_after": "country_code",
                "read_only": 0
            }
        ],
        "Sales Person": [
            {
                "fieldname": "vpa_id",
                "label": "VPA ID",
                "fieldtype": "Data",
                "insert_after": "employee",
                "read_only": 0
            },
            {
                "fieldname": "country_code",
                "label": "Country Code",
                "fieldtype": "Data",
                "insert_after": "vpa_id",
                "read_only": 0
            },
            {
                "fieldname": "mobile_no",
                "label": "Mobile No",
                "fieldtype": "Data",
                "insert_after": "country_code",
                "read_only": 0
            }
        ],
        # "Website Item": [
        #     {
        #         # "fieldname": "vpa_id",
        #         # "label": "VPA ID",
        #         # "fieldtype": "Data",
        #         # "insert_after": "employee",
        #         # "read_only": 0,
        #         "fieldname": "avaliable_at",
        #         "label": "Avaliable At",
        #         "fieldtype": "Table",
        #         "label": "Item Defaults",
        #         "options": "Item Default",
        #     }
        # ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            create_custom_field(doctype, field)

def create_custom_field(doctype, field):
    if not frappe.db.exists('Custom Field', {'dt': doctype, 'fieldname': field['fieldname']}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": doctype,
            **field
        })
        custom_field.insert(ignore_permissions=True)
        frappe.db.commit()




def add_role_profile():
    if not frappe.db.exists('Role Profile', 'io'):
        role_profile = frappe.get_doc({
            'doctype': 'Role Profile',
            'role_profile': 'io',
            'roles': [
                {'role': 'Customer'},
                {'role': 'Supplier'}
            ]
        })
        role_profile.insert(ignore_permissions=True)
        frappe.db.commit()





def add_item_group():
    if not frappe.db.exists('Item Group', 'Exchange'):
        item_group = frappe.get_doc({
            'doctype': 'Item Group',
            'item_group_name': 'Exchange',
            'parent_item_group': 'All Item Groups',
            'is_group': 0
        })
        item_group.insert(ignore_permissions=True)
        frappe.db.commit()

def create_commission_rate_field():
    if not frappe.db.exists('Custom Field', {'dt': 'Item', 'fieldname': 'commission_rate'}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Item",
            "fieldname": "commission_rate",
            "label": "Commission Rate",
            "fieldtype": "Percent",
            "insert_after": "standard_rate",
            "read_only": 0
        })
        custom_field.insert()
        frappe.db.commit()

def change_referral_code_length():
    # Fetch the current Doctype definition
    sales_partner_doctype = frappe.get_doc('DocType', 'Sales Partner')

    # Find the 'referral_code' field
    referral_code_field = None
    for field in sales_partner_doctype.fields:
        if field.fieldname == 'referral_code':
            referral_code_field = field
            break

    if referral_code_field:
        # Update the field length
        referral_code_field.length = 15
        sales_partner_doctype.save()

        # Update the schema in the database
        frappe.db.sql_ddl(f"""
            ALTER TABLE `tabSales Partner`
            MODIFY COLUMN `referral_code` VARCHAR(15);
        """)
    else:
        frappe.throw('Field "referral_code" not found in Sales Partner Doctype')

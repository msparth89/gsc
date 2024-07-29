import frappe
import string
import random
import requests
from frappe.utils import get_site_name
from frappe.auth import CookieManager, LoginManager
from frappe import auth

import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path
from frappe import _

REDIS_PREFIX = "otp"

@frappe.whitelist(allow_guest=True)
def generate_otp():
    print("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    return generate_otp_for_phone(frappe.form_dict.country_code,frappe.form_dict.phone_no)


@frappe.whitelist(allow_guest=True)
def verify_otp():
    phone = frappe.form_dict.country_code+frappe.form_dict.verify_otp
    key = f"{REDIS_PREFIX}:{phone}"
    cachedvalue = frappe.cache().get(key)

    # if cached_value:
    # decoded_value = cachedvalue.decode("utf-8")
    print(" --------------          ",cachedvalue)
    # else:
    print("No value found in cache for the specified key")
        # return verify_otp_for_phone(frappe.form_dict.country_code, frappe.form_dict.phone_no, frappe.form_dict.verify_otp)







def random_string_generator(str_size, allowed_chars):
    return "".join(random.choice(allowed_chars) for x in range(str_size))


def send_sms(phone, otp, domain):
    # Strip out + when sending SMS
    phone = phone.replace("+", "")
    url = "https://control.msg91.com/api/v5/flow/"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": frappe.conf["msg91_authkey"],
    }
    payload = {
        "template_id": frappe.conf["msg91_template_id"],
        "sender": frappe.conf.get("msg91_sender_id") or "IoTRDY",
        "short_url": "0",
        "mobiles": phone,
        "var1": domain,
        "var2": otp,
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def generate_otp_for_phone(country_code,phone_no):
    payload = {
        "success": False,
        "message": None,
    }
    phone = country_code+phone_no  # Set India as default
    print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", phone)
    otp = random_string_generator(4, string.digits)
    frappe.cache().set(f"{REDIS_PREFIX}:{phone}", otp, ex=300)

    key = f"{REDIS_PREFIX}:{phone}"
    # stored_otp = frappe.cache().get(key).decode("utf-8")
    stored_otp = frappe.cache().get(key)

    print(" 888888888888888888888         ------------         ",stored_otp)
    try:
        # send_sms(phone=phone, otp=otp, domain=domain)
        payload["success"] = True
        payload["otp"] = otp
        payload["message"] = f"OTP sent by SMS sent to {phone}"
    except Exception as e:
        print(str(e))
        payload["message"] = str(e)
    return payload


def verify_otp_for_phone(country_code,phone_no,otp):
    payload = {
        "success": False,
        "message": None,
    }
    # if phone[0] != "+":
        # phone = f"+91{phone}"  # Set India as default
    phone = country_code+phone_no
    key = f"{REDIS_PREFIX}:{phone}"
    stored_otp = frappe.cache().get(key).decode("utf-8")
    print(" 111111111111111111111111111         ------------         ",stored_otp)

    login_manager = frappe.auth.LoginManager()

    if not stored_otp == otp:
        payload["message"] = "Incorrect OTP."
        return payload
    try:
        user = frappe.db.get("User", {"mobile_no": phone_no,"country_code" : country_code})
    # if not user:
        # create_user(country_code,phone_no)
        # create_sales_partner(country_code,phone_no)
        # frappe.cache().delete_key(key)
        # login_manager.post_login()
    except Exception as e:
        payload["message"] = "User not found. and created one"
        create_user(country_code,phone_no)
        create_sales_partner(country_code,phone_no)
        return payload

    # Delete stored OTP

    # Now log in as user
    frappe.utils.set_request(path="/")
    frappe.local.cookie_manager = CookieManager()
    frappe.local.login_manager = LoginManager()
    return frappe.local.login_manager.login_as(user.name)





def create_user(country_code,phone_no):
    print("qqqqqqqqqqqqqqqqqqqqqqqq")
    if frappe.db.exists("User", {"mobile_no": phone_no,"country_code" : country_code}):
        frappe.throw(_("Mobile No already allocated to another User"))
    # if frappe.db.exists("User", {'email': self.personal_email}):
        # frappe.throw(_("Email ID is already allocated to another User"))
    site_name = get_site_name(frappe.local.request.host)    
    new_user = frappe.get_doc({
        "doctype": "User",
        "first_name": phone_no,
        "email": phone_no+"@"+site_name,
        "send_welcome_email": 0,
        "mobile_no": phone_no,
        "username": phone_no+site_name,
        "role_profile_name": 'io',
        "country_code" : country_code,
        # "roles": [{"doctype": "Has Role", "role": 'Customer'},
        # {"doctype": "Has Role", "role": 'Supplier'}]
    })
    try:
        new_user.insert(ignore_permissions=True)
    except:
        frappe.log_error(
            title="User creation error while creating new employee",
            message=frappe.get_traceback()
        )


def create_sales_partner(country_code,phone_no):
    print("qqqqqqqqqqqqqqqqqqqqqqqq")
    if frappe.db.exists("Sales Partner", {"mobile_no": phone_no,"country_code" : country_code, "Territory": "All Territories"}):
        Print("Sales Person No already allocated to another User")
    # if frappe.db.exists("User", {'email': self.personal_email}):
    #     frappe.throw(_("Email ID is already allocated to another User"))
    site_name = get_site_name(frappe.local.request.host) 
    new_user = frappe.get_doc({
        "doctype": "Sales Partner",
        "partner_name": phone_no+site_name,
        "commission_rate" : 10,
        "territory" : "All Territories",
        "partner_type" : "Agent",
        "mobile_no": phone_no,
        "country_code": country_code,
        "referral_code" : country_code+phone_no,
    })
    try:
        new_user.insert(ignore_permissions=True)
    except:
        frappe.log_error(
            title="User creation error while creating new employee",
            message=frappe.get_traceback()
        )







def custom_path_resolver(path):
    # Get the query parameters from the request
    print(path)
    query_params = frappe.form_dict
    print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    print(query_params)
    abc = query_params.get("abc")
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    print(abc)
    # return original_resolve_path(path)

    if abc:
        # Your logic to determine the redirect URL
        if abc == "some_value":
            print("000000000000000000000000000000000000000000000000000")
            redirect_url = "/app/doctype"
            return original_resolve_path(redirect_url)
        else:
            # redirect_url = "/default/redirect/url"
            redirect_url = "/circulate"
            # context["partner"] = abc
            print("111111111111111111111111111111111111111111111111111")
            return original_resolve_path(redirect_url)
            # return redirect_url

        # Return the redirect URL
        # return redirect_url
    else:
        print("2222222222222222222222222222222222222222222222222222222")
        # redirect_url = "/all-products/?sp=1233512345"
        # return redirect_url/
        redirect_url = "/circulate"
        return original_resolve_path(redirect_url)
        # return frappe.website.path_resolver.PathResolver(redirect_url)

        # return frappe.local.response["location"] = redirect_url
    # If no "abc" parameter, return None to continue normal routing
    return None


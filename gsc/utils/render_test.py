import frappe

def test_render_template():
    # Define the template file path
    template_path = "gsc/templates/sample_template.html"

    # Context data for rendering
    context = {
        "name": "Alice",
        "project": "Website Redesign"
    }

    # Read and render the template
    template_content = frappe.get_file(template_path).read()
    rendered_html = frappe.render_template(template_content, context)

    # Print the result or return it for further use
    print(rendered_html)
    return rendered_html

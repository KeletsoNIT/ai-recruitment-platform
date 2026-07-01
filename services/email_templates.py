import os

TEMPLATE_DIR = "templates"


def load_template(template_name, context):
    """
    Loads an email template and replaces placeholders.

    Args:
        template_name (str): interview, shortlisted, or rejection
        context (dict): values like name, job_title

    Returns:
        str: formatted email body
    """

    file_path = os.path.join(TEMPLATE_DIR, f"{template_name}.txt")

    # Read template file
    with open(file_path, "r") as file:
        template = file.read()

    # Replace placeholders safely
    for key, value in context.items():
        placeholder = "{" + key + "}"
        template = template.replace(placeholder, str(value))

    return template

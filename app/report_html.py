from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def save_html_report(report_data, template_dir="templates", output_file="outputs/report.html"):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("dashboard.html.j2")
    rendered = template.render(report=report_data)

    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")

    return str(path)
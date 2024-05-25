import jinja2
import pdfkit
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/generatePdf")
def generatePdf():
    requestBody = request.get_json()
    bestMatch = match()
    converted_html_path = modifyHTML(requestBody, bestMatch)

    print("converting...")
    
    pdf_path = f'./converted/sample_invoice{bestMatch}.pdf'
    html2pdf(converted_html_path, pdf_path)

    return "Created PDF!"

def html2pdf(html_path, pdf_path):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)


def match():
    return "1"


def modifyHTML(arguments, bestMatch):
    values = {}
    dataList = arguments["fields"]
    for data in dataList:
        values[data["fieldName"]] = data["actualValue"]
    
    template_loader = jinja2.FileSystemLoader(searchpath="./sample_invoice")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "sample_invoice" + bestMatch + ".html"
    template = template_env.get_template(template_file)
    output_text = template.render(
        values
        )

    converted_html_path = f'./converted/sample_invoice{bestMatch}.html' 
    try:
        html_file = open(converted_html_path, 'x')
    except:
        html_file = open(converted_html_path, 'w')

    html_file.write(output_text)
    html_file.close()
    return converted_html_path

@app.route("/aiRetriever")
def aiRetriever():
    requestBody = request.get_json()
    if (requestBody["templateType"] == "freeText"):
        return serve_response(requestBody["freeText"])

def serve_response(query):
    #return RESPONSE_DICT
    pass

if __name__ == "__main__":
    app.run()
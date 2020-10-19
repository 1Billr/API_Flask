from xhtml2pdf import pisa
import jinja2
from multiprocessing import Pool

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "sample-bill.html"
CSS_FILE = "static/styles.css"
template = templateEnv.get_template(TEMPLATE_FILE)


def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
        src=sourceHtml, dest=resultFile  # the HTML to convert
    )  # file handle to receive result

    # close output file
    resultFile.close()

    # return True on success and False on errors
    print(pisaStatus.err, type(pisaStatus.err))
    return pisaStatus.err


def generate_pdf(data, details):
    sourceHtml = template.render(json_data=data, details_data=details, css=CSS_FILE)
    outputFilename = "gen_bills/" + str(details["customerPhoneNumber"]) + "-invoice.pdf"
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)
    return outputFilename

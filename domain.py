from xhtml2pdf import pisa
import jinja2
from multiprocessing import Pool
import os

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


def generate_folder(customerPhoneNumber, storeName):
    base_path = "static/db/"
    file_paths = [
        "static",
        "static/db",
        base_path + customerPhoneNumber,
        base_path + customerPhoneNumber + "/" + storeName + "/",
    ]
    for path in file_paths:
        if not os.path.exists(path):
            os.makedirs(path)
    return file_paths[-1]


def generate_pdf(data, storeData):
    file_path = generate_folder(
        str(data["customerPhoneNumber"]), str(storeData["name"])
    )
    sourceHtml = template.render(data=data, storeData=storeData, css=CSS_FILE)
    amountTotal = str(data["invoiceAmount"])
    outputFilename = (
        file_path
        + data["createdAt"].strftime("%Y%m%d%H%M%S")
        + "_"
        + amountTotal
        + ".pdf"
    )
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)
    return outputFilename

from flask import Flask, render_template, request, send_file, redirect
from pdfrw import PdfReader, PdfWriter, PageMerge
from dotenv import load_dotenv
from livereload import Server
import subprocess
import zipfile
import os

# Loads ambient variables
load_dotenv()

# Reads and converts te DEBUG ambient variable
debug_mode = os.getenv('DEBUG', 'False') == 'True'  # Defaults to False

app = Flask(__name__)

# Set debug mode in flask based on ambient variable
app.debug = debug_mode

# Configs for file upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['WATERMARK_FOLDER'] = 'static/watermarks'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc'}

# Function to verify if the file has the correct extension
def checkAllowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to convert .docx files in .pdf using headless libreoffice 
def convertDocxToPdf(inputFile):
    inputDir = os.path.dirname(inputFile)
    outputFile = os.path.join(inputDir, os.path.basename(inputFile).rsplit('.', 1)[0] + '.pdf')
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', inputDir, inputFile])
    return outputFile

# Function to apply the watermark to the file (from official repo https://github.com/pmaupin/pdfrw/blob/master/examples/fancy_watermark.py)
def addWatermarkToPdf(inputFile, outputFile, watermarkFile):
 
    # Open both the source files
        watermarkTrailer = PdfReader(watermarkFile)
        trailer = PdfReader(inputFile)

        # Handle different sized pages in same document with
        # a memoization cache, so we don't create more watermark
        # objects than we need to (typically only one per document).

        watermarkPage = watermarkTrailer.pages[0]
        watermarkCache = {}

        # Process every page
        for pagenum, page in enumerate(trailer.pages, 1):

            # Get the media box of the page, and see
            # if we have a matching watermark in the cache
            mbox = tuple(float(x) for x in page.MediaBox)
            odd = pagenum & 1
            key = mbox, odd
            wmark = watermarkCache.get(key)
            if wmark is None:

                # Create and cache a new watermark object.
                wmark = watermarkCache[key] = PageMerge().add(watermarkPage)[0]

                # The math is more complete than it probably needs to be,
                # because the origin of all pages is almost always (0, 0).
                # Nonetheless, we illustrate all the values and their names.

                page_x, page_y, page_x1, page_y1 = mbox
                page_w = page_x1 - page_x                

                # Scale the watermark if it is too wide for the page
                # (Could do the same for height instead if needed)
                if wmark.w > page_w:
                    wmark.scale(1.0 * page_w / wmark.w)

                # Always put watermark at the top of the page
                # (but see horizontal positioning for other ideas)
                wmark.y += page_y1 - wmark.h

                # For odd pages, put it at the left of the page,
                # and for even pages, put it on the right of the page.
                if odd:
                    wmark.x = page_x
                else:
                    wmark.x += page_x1 - wmark.w

                # Optimize the case where the watermark is same width
                # as page.
                if page_w == wmark.w:
                    watermarkCache[mbox, not odd] = wmark

            # Add the watermark to the page
            PageMerge(page).add(wmark, prepend=False).render()

        # Write out the destination file
        PdfWriter(outputFile, trailer=trailer).write()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():

    # If there aren't documents in the request, redirect to the index page
    if 'documents' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('documents')
    
    # If the files are not in the valid formats, return an error
    if not files or any(file is None or not checkAllowedFile(file.filename) for file in files):
        return "File non valido", 400

    # Try to parse the opacity value, set standard at 15
    try:
        opacity = int(request.form["opacity"])
    except (ValueError, TypeError):        
        opacity = 15

    # Set the opacity value in the correct range
    if opacity < 0 or opacity > 30:
        opacity = 15  # if it's not in the correct range, set to 15 at default

    # Try to parse the staff value, set standard to "Ingegneria"
    try:
        staff = request.form["staff"]
    except (ValueError, TypeError):
        staff = "Ingegneria"

    # Check if the logo checkbox has been selected
    logo = "logo" in request.form

    # All the files which will be sent to the user
    outputFiles = []

    # Foreach file, save it, convert it, apply watermark, send it and then delete it
    for file in files:

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the file in the upload folder
        file.save(filepath)

        # Set the outputFile path as a combination of the upload folder, the name of the file and the pdf extension
        outputFile = os.path.join(app.config['UPLOAD_FOLDER'], f'watermarked_{os.path.splitext(filename)[0]}.pdf')

        # Set the watermarkPath as a combination of the watermarks folder, the staff, the opacity and the presence or absence of the logo, at last the pdf extension
        filigranaPath = os.path.join(app.config['WATERMARK_FOLDER'], staff,f'fil_{opacity}{'_logo' if logo else ''}_ver.pdf')

        # If the watermark wasn't found, throw an error
        if not os.path.exists(filigranaPath):
            return "Watermark non trovato", 404

        # Check if the file is a .docx file
        if filename.lower().endswith('.docx'):
            # If so, convert it to pdf
            convertedPdfPath = convertDocxToPdf(filepath)

            # After converting, we've got the .pdf file path, so we can remove the .docx file
            os.remove(filepath)
            filepath = convertedPdfPath

        # Now, apply the watermark to the .pdf file 
        addWatermarkToPdf(filepath, outputFile, filigranaPath)
        
        # Add the watermarked file in the outputFiles array
        outputFiles.append(outputFile)

        # Remove the not watermarked pdf of the file
        if os.path.exists(filepath):
            os.remove(filepath)
        
    # Prepare the zip output path in case we need it later (if there are more than 1 file)
    zipOutput = ""

    # If we've got only 1 file
    if len(outputFiles) == 1:
        try:
            # Return the watermarked file as an attachment
            return send_file(outputFiles[0], as_attachment=True)
        finally:
            # When the watermarked file is returned, remove it from disk
            if os.path.exists(outputFiles[0]):
                os.remove(outputFiles[0])

    # Otherwise, if we've got more than 1 file
    try:

        # Prapare the zip path as the upload folder and a generic zip name
        zipOutput = os.path.join(app.config['UPLOAD_FOLDER'], 'File filigranati.zip')

        # Open the zip path
        with zipfile.ZipFile(zipOutput, 'w') as zipf:
            # Foreach file, zip it in the same archive
            for file in outputFiles:
                zipf.write(file, os.path.basename(file))
        
        # Remove the files from the outputFiles array
        for file in outputFiles:
            if os.path.exists(file):
                os.remove(file)

        # Send the zip file as an attachment
        return send_file(zipOutput, as_attachment=True)
    
    finally:
        # When the watermarked zip file is returned, remove it from disk
        if os.path.exists(zipOutput):
            os.remove(zipOutput)

# Set Livereload service
if __name__ == '__main__':
    server = Server(app.wsgi_app)  
    server.watch('./templates/**')  # Monitor templates directory
    server.watch('./static/**')     # Monitors static directory
    server.serve(port=5000)         # Starts server on port 5000
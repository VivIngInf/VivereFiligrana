from flask import Flask, render_template, request, send_file, redirect
from pdfrw import PdfReader, PdfWriter, PageMerge
from dotenv import load_dotenv
from livereload import Server
import subprocess
import os
import zipfile

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
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Funzione per la conversione DOCX -> PDF usando LibreOffice in modalità headless
def convert_docx_to_pdf(input_file):
    input_dir = os.path.dirname(input_file)
    output_file = os.path.join(input_dir, os.path.basename(input_file).rsplit('.', 1)[0] + '.pdf')
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', input_dir, input_file])
    return output_file

# Function to apply the watermark to the file (from official repo https://github.com/pmaupin/pdfrw/blob/master/examples/fancy_watermark.py)
def add_watermark_pdf(input_file, output_file, watermark_file):
 
    # Open both the source files
        wmark_trailer = PdfReader(watermark_file)
        trailer = PdfReader(input_file)

        # Handle different sized pages in same document with
        # a memoization cache, so we don't create more watermark
        # objects than we need to (typically only one per document).

        wmark_page = wmark_trailer.pages[0]
        wmark_cache = {}

        # Process every page
        for pagenum, page in enumerate(trailer.pages, 1):

            # Get the media box of the page, and see
            # if we have a matching watermark in the cache
            mbox = tuple(float(x) for x in page.MediaBox)
            odd = pagenum & 1
            key = mbox, odd
            wmark = wmark_cache.get(key)
            if wmark is None:

                # Create and cache a new watermark object.
                wmark = wmark_cache[key] = PageMerge().add(wmark_page)[0]

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
                    wmark_cache[mbox, not odd] = wmark

            # Add the watermark to the page
            PageMerge(page).add(wmark, prepend=False).render()

        # Write out the destination file
        PdfWriter(output_file, trailer=trailer).write()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'documents' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('documents')
    
    if not files or any(file is None or not allowed_file(file.filename) for file in files):
        return "File non valido", 400

    try:
        opacity = int(request.form["opacity"])
    except (ValueError, TypeError):
        # Se il valore non è valido (non numerico o non presente), assegna un valore di default
        opacity = 5

    # Assicurati che opacity sia nel range accettabile
    if opacity < 0 or opacity > 30:
        opacity = 5  # valore di default se non è valido

    logo = "logo" in request.form

    # Ciclo sui file per salvarli, convertirli e applicare la filigrana
    output_files = []

    for file in files:

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        output_file = os.path.join(app.config['UPLOAD_FOLDER'], f'watermarked_{os.path.splitext(filename)[0]}.pdf')
        filigrana_path = os.path.join(app.config['WATERMARK_FOLDER'], f'fil_{opacity}{'_logo' if logo else ''}_ver.pdf')

        if not os.path.exists(filigrana_path):
            return "Watermark non trovato", 404

        if filename.lower().endswith('.docx'):
            # Converti il DOCX in PDF prima di applicare il watermark
            converted_pdf_path = convert_docx_to_pdf(filepath)

            # Dopo la conversione, rimuovi il file DOCX
            os.remove(filepath)
            filepath = converted_pdf_path

        add_watermark_pdf(filepath, output_file, filigrana_path)
        
        # Aggiungi il file con la filigrana alla lista di output
        output_files.append(output_file)

        # Cancellazione dei file temporanei
        if os.path.exists(filepath):
            os.remove(filepath)  # Rimuove il file caricato
        
    zip_output = ""

    if len(output_files) == 1:
        try:
            # Restituisci i file con la filigrana per il download
            return send_file(output_files[0], as_attachment=True)
        finally:
            if os.path.exists(output_files[0]):
                os.remove(output_files[0])

    try:
        zip_output = os.path.join(app.config['UPLOAD_FOLDER'], 'watermarked_files.zip')
        with zipfile.ZipFile(zip_output, 'w') as zipf:
            for file in output_files:
                zipf.write(file, os.path.basename(file))
        
        # Rimuovi i file temporanei
        for file in output_files:
            if os.path.exists(file):
                os.remove(file)

        return send_file(zip_output, as_attachment=True)
    
    finally:
        if os.path.exists(zip_output):
            os.remove(zip_output)

# Set Livereload service
if __name__ == '__main__':
    server = Server(app.wsgi_app)  
    server.watch('./templates/**')  # Monitor templates directory
    server.watch('./static/**')     # Monitors static directory
    server.serve(port=5000)         # Starts server on port 5000
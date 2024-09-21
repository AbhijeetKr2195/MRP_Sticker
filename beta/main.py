import io
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from flask import Flask, render_template, request, send_file
from Ceiling_Fan import ceiling_mrp_sticker
from Ceiling_Fan_U import ceiling_U_mrp_sticker
from TPW import generate_mrp_sticker

app = Flask(__name__)

@app.route('/generate_mrp')
def form():
    return render_template('generate_mrp.html')
  
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # GET FORM DATA
    Catogary = request.form.get('catogary', "Stand Fan").upper()
    Model = request.form.get('model', "Windy").upper()
    Content = request.form.get('content', "1").strip().upper().split()[0]
    MRP = request.form.get('mrp', "3,780")
    MFD = request.form.get('mfd', "SEPTEMBER 2024").upper()
    MFD_AT = request.form.get('mfd_at', "88/C IDA JEEDIMETLA PHASE III Hyderabad - 500055").upper()
    image_path = "p.png"
    image_path1 = "a.png"
    print(Content)
    if Catogary in ["STAND FAN", "WALL FAN", "TABLE FAN"]:
        pdf_buffer = generate_mrp_sticker(Catogary, Model, Content, MRP, MFD, MFD_AT, image_path)
    
    elif Catogary == "CEILING FAN":
        if Content == "1":
            pdf_buffer = ceiling_mrp_sticker(Catogary, Model, Content, MRP, MFD, MFD_AT, image_path, image_path1)  # Make sure this matches the definition
        else:
            pdf_buffer = ceiling_U_mrp_sticker(Catogary, Model, Content, MRP, MFD, MFD_AT, image_path, image_path1)


    pdf_buffer.seek(0)

    # SEND THE PDF AS A FILE DOWNLOAD
    return send_file(pdf_buffer, as_attachment=True, download_name=f"MRP_Sticker_Of_{Model}_{Catogary}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

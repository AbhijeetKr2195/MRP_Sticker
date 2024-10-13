from flask import Flask, render_template, request, send_file

from Universal_Template import universal_mrp_sticker
from Ceiling_Fan_Template import ceiling_mrp_sticker
from Universal_Templates_Unite import universal_mrp_sticker_unites
from Immersion_Heater_Template import immersion_heater_mrp_sticker

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('generate_mrp.html')
  
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    Catogary = request.form.get('catogary', "Stand Fan").upper()
    Model = request.form.get('model', "Windy").upper()
    Content = request.form.get('content', "1").strip().upper().split()[0]
    MRP = request.form.get('mrp', "3,780")
    MFD = request.form.get('mfd', "SEPTEMBER 2024").upper()
    MFD_AT = request.form.get('mfd_at', "88/C IDA Jeedimetla Phase III Hyderabad - 500055")
    image_path = "rally.png"
    image_path1 = "india.png" 

    if Catogary in ["STAND FAN", "WALL FAN", "TABLE FAN"]:
        if Content == "1":
            pdf_buffer = universal_mrp_sticker(Catogary, Model, Content, MRP, MFD, MFD_AT, image_path)
        else:
            pdf_buffer = universal_mrp_sticker_unites(Catogary, Model, Content, MRP, MFD, MFD_AT)
    
    elif Catogary == "CEILING FAN":
        if Content == "1":
            pdf_buffer = ceiling_mrp_sticker(Catogary, Model, Content, MRP, MFD, MFD_AT, image_path, image_path1)
        else:
            pdf_buffer = universal_mrp_sticker_unites(Catogary, Model, Content, MRP, MFD, MFD_AT)

    elif Catogary == "IMMERSION HEATER":
        if Content == "1":
            pdf_buffer = immersion_heater_mrp_sticker(category=Catogary, model=Model, content=Content, mrp=MRP, mfd=MFD, mfd_at=MFD_AT, image_path=image_path)
        else:
            pdf_buffer = universal_mrp_sticker_unites(Catogary, Model, Content, MRP, MFD, MFD_AT)

    else:
        if Content == "1":
            pdf_buffer = universal_mrp_sticker(Catogary, Model, Content, MRP, MFD, MFD_AT, image_path)
        else:
            pdf_buffer = universal_mrp_sticker_unites(Catogary, Model, Content, MRP, MFD, MFD_AT)

    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"MRP_Sticker_Of_{Model}_{Catogary}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

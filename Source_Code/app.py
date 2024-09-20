import io
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/generate_mrp')
def form():
    return render_template('generate_mrp.html')
  
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # GET FORM DATA
    Catogary = request.form.get('catogary', "Stand Fan").upper()
    Model = request.form.get('model', "Windy").upper()
    Content = request.form.get('content', "1 UNIT OF").upper()
    MRP = request.form.get('mrp', "3,780")
    MFD = request.form.get('mfd', "SEPTEMBER 2024").upper()
    MFD_AT = request.form.get('mfd_at', "88/C IDA JEEDIMETLA PHASE III Hyderabad - 500055").upper()
    image_path = "Rally_Logo.png"
  
    # DIMENSIONS: 100 MM X 75 MM
    width, height = 100 * mm, 75 * mm

    # CREATE A PDF IN MEMORY
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=(width, height))

    # INSET THE BORDER BY 3 MM FROM EACH EDGE
    border_inset = 3 * mm
    border_width = width - 2 * border_inset
    border_height = height - 2 * border_inset

    # DRAW A BORDER INSET BY 3 MM
    pdf.rect(border_inset, border_inset, border_width, border_height)

    # FUNCTION TO ADD WRAPPED TEXT
    def add_wrapped_text(pdf, text, x, y, font, size, max_width):
        pdf.setFont(font, size)
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if pdf.stringWidth(current_line + word + " ", font, size) <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        for line in lines:
            pdf.drawString(x, y, line)
            y -= size + 2

    # FUNCTION TO ADD A LINE
    def add_line(pdf, x, y, end_x):
        pdf.line(x, y, end_x, y)

    # FUNCTION TO ADD IMAGE
    def add_image(pdf, image_path, x, y, width, height):
        img = ImageReader(image_path)
        pdf.drawImage(img, x, y, width, height)

    # TEXT POSITION INSIDE THE BORDER (ADJUST AS NECESSARY)
    font = "Helvetica-Bold"
    size = 10
    text_margin = 5 * mm
    max_text_width = border_width - 2 * text_margin

    x1 = border_inset + text_margin
    y1 = height - 8 * mm

    add_wrapped_text(pdf, f"Content: {Content} of {Catogary}", x=x1, y=y1, font=font, size=size, max_width=max_text_width)
    y2 = y1 - (size + 8)
    add_wrapped_text(pdf, f"MRP: Rs {MRP}.00/- (Incl of All Taxes)", x=x1, y=y2, font=font, size=size, max_width=max_text_width)
    y3 = y2 - (size + 8)
    add_wrapped_text(pdf, f"Month of MFD: {MFD}", x=x1, y=y3, font=font, size=size, max_width=max_text_width)

    small_font_size = 6
    y4 = y3 - (small_font_size + 9)
    add_wrapped_text(pdf, "Customer Care Address & Mktd by: Mahavir Home Appliances", x=x1, y=y4, font=font, size=small_font_size, max_width=max_text_width)

    address_font_size = 9
    y5 = y4 - (address_font_size + 4)
    add_wrapped_text(pdf, "#137/2, 1st Main, 3rd Cross New Timberyard Layout Mysore Road, Bangalore - 560026", x=x1, y=y5, font=font, size=address_font_size, max_width=max_text_width)

    y6 = y5 - (address_font_size + 13)
    add_wrapped_text(pdf, "For Service Contact:", x=x1, y=y6, font=font, size=address_font_size, max_width=max_text_width)

    y7 = y6 - (address_font_size + 4)
    add_wrapped_text(pdf, "Toll Free No.: 080-61977979, 18001026019", x=x1, y=y7, font=font, size=address_font_size, max_width=max_text_width)

    y8 = y7 - (address_font_size + 4)
    add_wrapped_text(pdf, "Email Id: customercare@rallyappliances.com", x=x1, y=y8, font=font, size=address_font_size, max_width=max_text_width)

    y9 = y8 - (small_font_size + 4)
    add_wrapped_text(pdf, "Timing: 10:30am to 5:00pm(Sunday Holiday)", x=x1, y=y9, font=font, size=small_font_size, max_width=max_text_width)

    y10 = y9 - (address_font_size + 4)
    add_wrapped_text(pdf, f"Mfd at: {MFD_AT}", x=x1, y=y10, font=font, size=address_font_size, max_width=max_text_width)

    y11 = y10 - (address_font_size + 20)
    add_wrapped_text(pdf, f"{Catogary} - {Model}:    Rs {MRP}.00/-", x=x1, y=y11, font=font, size=address_font_size, max_width=max_text_width)

    add_line(pdf, border_inset, y1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y3 - 2 * mm, width - border_inset)

    # ADD IMAGE TO THE PDF
    image_width = 18 * mm
    image_height = 18 * mm
    x_image = border_inset + 75 * mm
    y_image = border_inset + 21 * mm
    add_image(pdf, image_path, x_image, y_image, image_width, image_height)

    # SAVE PDF TO THE BUFFER
    pdf.save()
    pdf_buffer.seek(0)

    # SEND THE PDF AS A FILE DOWNLOAD
    return send_file(pdf_buffer, as_attachment=True, download_name=f"MRP_Sticker_Of_{model}_{catogary}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

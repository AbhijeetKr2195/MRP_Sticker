import io
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from utils import add_wrapped_text, add_line, add_image, draw_labeled_text_with_wrap

# REGISTER CUSTOM FONTS
pdfmetrics.registerFont(TTFont('Monstera_Bold', 'Monstera_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Monstera_Thin', 'Monstera_Thin.ttf'))

def universal_mrp_sticker(category, model, content, mrp, mfd, mfd_at, image_path):
    # DEFINE PDF DIMENSIONS
    width, height = 100 * mm, 75 * mm
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    # DEFINE BORDER DIMENSIONS
    border_inset = 3 * mm
    border_width = width - 2 * border_inset
    border_height = height - 2 * border_inset
    pdf.rect(border_inset, border_inset, border_width, border_height)

    # SET FONTS AND SIZES
    font_a = "Monstera_Bold"
    font = "Monstera_Thin"
    size = 10
    text_margin = 2 * mm
    max_text_width = border_width - 2 * text_margin

    # INITIAL TEXT POSITIONING
    x1 = border_inset + text_margin
    y1 = height - 8 * mm

    # ADD CONTENT TEXT
    add_wrapped_text(pdf, f"Content             :  {content} UNIT OF {category}", x=x1, y=y1, font=font, size=size, max_width=max_text_width)

    address_font_size = 9
    # ADD MODEL TEXT
    y1_yy = y1 - (10 + 8)
    add_wrapped_text(pdf, f"Model                 :  {model}", x=x1, y=y1_yy, font=font, size=10, max_width=max_text_width)

    # ADD MRP TEXT
    y2 = y1_yy - (size + 8)
    y2_1 = y1_yy - (size + 8)

    pdf.setFont(font_a, 10)
    pdf.drawString(x=x1, y=y2_1, text="MRP                  :         ")

    pdf.setFont(font_a, 10)
    pdf.drawString(x=x1 + pdf.stringWidth("MRP            ", font, 10), y=y2, text=f"          ₹ {mrp}.00/- (Incl. Of All Taxes)")

    # ADD MANUFACTURE DATE TEXT
    y3 = y2 - (size + 8)
    add_wrapped_text(pdf, f"Month of MFD :  {mfd}", x=x1, y=y3, font=font, size=size, max_width=max_text_width)

    small_font_size = 6
    address_font_size = 9
    y4 = y3 - (8 + 8)

    # ADD CUSTOMER CARE ADDRESS LABEL
    label_text = "Customer Care Address & Mkd By : "
    pdf.setFont(font_a, 8)
    label_text_width = pdf.stringWidth(label_text, font, 8)
    pdf.drawString(x1, y4, label_text)

    new_x_position_address = x1 + label_text_width

    # ADD CUSTOMER CARE ADDRESS TEXT
    pdf.setFont(font, 8)
    pdf.drawString(new_x_position_address, y4, "    Mahavir Home Appliances")

    # ADD ADDRESS TEXT
    y5 = y4 - (address_font_size + 4)
    add_wrapped_text(pdf, "#137/2, 1st Main, 3rd Cross New Timberyard Layout Mysore Road, Bangalore - 560026", x=x1, y=y5, font=font, size=address_font_size, max_width=max_text_width)

    # ADD SERVICE CONTACT LABEL
    y6 = y5 - (address_font_size + 16)
    add_wrapped_text(pdf, "For Service Contact:", x=x1, y=y6, font=font, size=address_font_size, max_width=max_text_width)

    # ADD TOLL FREE NUMBER
    y7 = draw_labeled_text_with_wrap(pdf, 
                                    label="Toll Free No.: ", 
                                    text="08061977979, 18001026019", 
                                    x=x1, 
                                    y=y6 - (address_font_size + 4),
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=9, 
                                    text_size=8, 
                                    max_width=max_text_width)

    # ADD EMAIL ADDRESS
    y8 = draw_labeled_text_with_wrap(pdf, 
                                    label="Email Id: ", 
                                    text="customercare@rallyappliances.com", 
                                    x=x1, 
                                    y=y7,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=9, 
                                    text_size=8, 
                                    max_width=max_text_width)

    # ADD TIMINGS
    y9 = draw_labeled_text_with_wrap(pdf, 
                                    label="Timings: ", 
                                    text="10:30 AM to 5:00 PM (Sunday Holiday)", 
                                    x=x1, 
                                    y=y8,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=9, 
                                    text_size=8, 
                                    max_width=max_text_width)

    # ADD MANUFACTURE LOCATION
    y10 = draw_labeled_text_with_wrap(pdf, 
                                    label="Mfd at: ", 
                                    text=f"{mfd_at.title()}", 
                                    x=x1, 
                                    y=y9,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=9, 
                                    text_size=8, 
                                    max_width=max_text_width)

    # ADD HORIZONTAL LINES FOR SEPARATION
    add_line(pdf, border_inset, y1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y1_yy - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y3 - 2 * mm, width - border_inset)

    # ADD IMAGE TO PDF
    image_width = 17 * mm  
    image_height = 16 * mm  
    x_image = border_inset + 75 * mm  
    y_image = border_inset + 16 * mm  
    add_image(pdf, image_path, x_image, y_image, image_width, image_height)

    # SAVE THE PDF TO BUFFER
    pdf.save()

    buffer.seek(0)
    return buffer

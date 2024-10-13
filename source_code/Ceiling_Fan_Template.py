import io
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from utils import add_wrapped_text, add_line, add_image

# REGISTER CUSTOM FONTS
pdfmetrics.registerFont(TTFont('Monstera_Bold', 'Monstera_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Monstera_Thin', 'Monstera_Thin.ttf'))

def ceiling_mrp_sticker(Catogary, Model, Content, MRP, MFD, MFD_AT, image_path, image_path1):
    # SET UP PDF DIMENSIONS
    width, height = 100 * mm, 75 * mm
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    border_inset = 3 * mm
    border_width = width - 2 * border_inset
    border_height = height - 2 * border_inset

    # DRAW BORDER RECTANGLE
    pdf.rect(border_inset, border_inset, border_width, border_height)

    font_a = "Monstera_Bold"
    font = "Monstera_Thin"
    size = 9
    address_font_size = 8
    mrp_font_size = 12
    original_font_size = 10
    text_margin = 5 * mm
    max_text_width = border_width - 2 * text_margin

    x1 = border_inset + 3 * mm 
    y1 = height - 7 * mm  
    
    # ADD ITEM MODEL TEXT
    add_wrapped_text(pdf, f"ITEM                    :   {Model}", x=x1, y=y1, font=font, size=size, max_width=max_text_width)

    # ADD CONTENT TEXT
    y3 = y1 - (size + 8)
    add_wrapped_text(pdf, f"Content              :   {Content} Unit of {Catogary}", x=x1, y=y3, font=font, size=size, max_width=max_text_width)

    # ADD MRP LABEL
    y4 = y3 - (size + 8)
    y4_1 = y3 - (size + 8)
    
    pdf.setFont(font_a, mrp_font_size)
    pdf.drawString(x=x1, y=y4_1, text="MRP            :         ")

    # ADD MRP VALUE
    pdf.setFont(font_a, original_font_size)
    pdf.drawString(x=x1 + pdf.stringWidth("MRP            ", font, mrp_font_size), y=y4, text=f"    ₹ {MRP}.00/-")

    # ADD TAX INCLUSION NOTICE
    y5 = y4 - (address_font_size + 4)
    add_wrapped_text(pdf, "(Inclusive Of All Taxes)", x=x1 + 28 * mm, y=y5, font=font_a, size=address_font_size, max_width=max_text_width)

    # ADD MANUFACTURE DATE
    y6 = y5 - (size + 8)
    add_wrapped_text(pdf, f"Date Of MFD      :    {MFD}", x=x1, y=y6, font=font, size=size, max_width=max_text_width)

    # ADD VOLTAGE SPECIFICATION
    y2_2 = y6 - (size + 8)
    add_wrapped_text(pdf, "220-240 Volts, 50/60 Hz", x=x1, y=y2_2, font=font, size=size, max_width=max_text_width)

    # ADD CUSTOMER CARE ADDRESS LABEL
    y7 = y2_2 - (address_font_size + 7)
    label_text = "Customer Care Address & Mkd By: "
    pdf.setFont(font_a, address_font_size)
    label_text_width = pdf.stringWidth(label_text, font_a, address_font_size)
    pdf.drawString(x1, y7, label_text)

    # ADD CUSTOMER CARE ADDRESS
    new_x_position_address = x1 + label_text_width
    pdf.setFont(font, address_font_size)
    pdf.drawString(new_x_position_address, y7, "Mahavir Home Appliances")

    # ADD FULL ADDRESS
    y8 = y7 - (address_font_size + 4)
    add_wrapped_text(pdf, "#137/2, 1st Main, 3rd Cross New Timberyard Layout Mysore Road, Bangalore - 560026", x=x1, y=y8, font=font, size=7, max_width=max_text_width)

    # ADD EMAIL LABEL
    y10 = y8 - (address_font_size + 14)
    email_text = "E-mail: "
    pdf.setFont(font_a, address_font_size)
    email_text_width = pdf.stringWidth(email_text, font_a, address_font_size)
    pdf.drawString(x1, y10, email_text)

    # ADD EMAIL ADDRESS
    new_x_position_email = x1 + email_text_width
    new_y_position_email = y10
    add_wrapped_text(pdf, "customercare@rallyappliances.com", x=new_x_position_email, y=new_y_position_email, font=font, size=address_font_size, max_width=max_text_width - email_text_width)

    # ADD TOLL FREE LABEL
    y11 = y10 - (address_font_size + 3)
    toll_free_text = "Toll Free No.: "
    pdf.setFont(font_a, address_font_size)
    toll_free_text_width = pdf.stringWidth(toll_free_text, font_a, address_font_size)
    pdf.drawString(x1, y11, toll_free_text)

    # ADD TOLL FREE NUMBER
    new_x_position_toll_free = x1 + toll_free_text_width
    new_y_position_toll_free = y11
    add_wrapped_text(pdf, "08061977979 | 18001026019", x=new_x_position_toll_free, y=new_y_position_toll_free, font=font, size=address_font_size, max_width=max_text_width - toll_free_text_width)

    # ADD TIMINGS LABEL
    y12 = y11 - (address_font_size + 4)
    timings_text = "Timings: "
    pdf.setFont(font_a, address_font_size)
    timings_text_width = pdf.stringWidth(timings_text, font_a, address_font_size)
    pdf.drawString(x1, y12, timings_text)

    # ADD TIMINGS DETAILS
    new_x_position_timings = x1 + timings_text_width
    new_y_position_timings = y12
    add_wrapped_text(pdf, "10:30 AM to 5:00 PM (Sunday Holiday)", x=new_x_position_timings, y=new_y_position_timings, font=font, size=address_font_size, max_width=max_text_width - timings_text_width)

    # ADD MANUFACTURE LOCATION LABEL
    y13 = y12 - (address_font_size + 4)
    pdf.setFont(font_a, 7)
    mfd_text = "Mfd at: "
    mfd_text_width = pdf.stringWidth(mfd_text, font_a, address_font_size)
    pdf.drawString(x1, y13, mfd_text)

    # ADD MANUFACTURE LOCATION
    new_x_position = x1 + mfd_text_width
    new_y_position = y13
    add_wrapped_text(pdf, MFD_AT, x=new_x_position, y=new_y_position, font=font, size=address_font_size, max_width=max_text_width - mfd_text_width)

    # DRAW SEPARATING LINES
    add_line(pdf, border_inset, y1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2_2 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y3 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y5 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y6 - 2 * mm, width - border_inset)

    # ADD IMAGES TO PDF
    add_image(pdf, image_path, x=border_inset + 83 * mm, y=border_inset + 47 * mm, width=10 * mm, height=9 * mm)
    add_image(pdf, image_path1, x=border_inset + 72 * mm, y=border_inset + 16 * mm, width=20 * mm, height=9 * mm)

    # SAVE PDF TO BUFFER
    pdf.save()
    buffer.seek(0)
    return buffer

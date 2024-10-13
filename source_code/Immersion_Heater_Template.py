import io
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from utils import add_wrapped_text, draw_labeled_text_with_fit, draw_labeled_text_with_wrap, fit_text_in_box, add_image

# REGISTER CUSTOM FONTS
pdfmetrics.registerFont(TTFont('Monstera_Bold', 'Monstera_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Monstera_Thin', 'Monstera_Thin.ttf'))

def immersion_heater_mrp_sticker(category, model, content, mrp, mfd, mfd_at, image_path, volt="220-240V, 50Hz, AC"):
    # SET UP PDF DIMENSIONS
    width, height = 50 * mm, 50 * mm
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    border_inset = 1 * mm
    border_width = width - 2 * border_inset
    border_height = height - 2 * border_inset

    # DRAW BORDER RECTANGLE
    pdf.rect(border_inset, border_inset, border_width, border_height)

    # SET FONTS AND SIZES
    font_a = "Monstera_Bold"
    font = "Monstera_Thin"
    size = 8
    text_margin = 1 * mm
    max_text_width = border_width - 3 * text_margin
    
    # INITIAL TEXT POSITIONING
    x1 = border_inset + text_margin
    y1 = height - 4 * mm

    # ADD ITEM TEXT
    fit_text_in_box(pdf, f"ITEM :  1 UNIT OF IMMERSION HEATER", x1, y1, font, 16, max_text_width)

    # ADD MODEL TEXT
    y2 = y1 - 3 * mm
    fit_text_in_box(pdf, f"MODEL :  {model}", x1, y2, font, 8, max_text_width)

    small_size = 6
    # ADD VOLTAGE TEXT
    y4 = y2 - 4 * mm
    add_wrapped_text(pdf, f"VOLTS        :  {volt}", x=x1, y=y4, font=font, size=6, max_width=max_text_width)

    # ADD MRP TEXT
    y6_1 = y4 - 4 * mm
    add_wrapped_text(pdf, f"MRP      :  ₹ {mrp}", x=x1, y=y6_1, font=font_a, size=size, max_width=max_text_width)

    small_size = 5
    # ADD TAX INCLUSION NOTICE
    y7 = y6_1 - 2 * mm
    add_wrapped_text(pdf, "(Incl. of all taxes)", x=x1 + 40, y=y7, font=font_a, size=small_size, max_width=max_text_width)

    # ADD MANUFACTURE DATE TEXT
    y5_1 = y7 - 4 * mm
    add_wrapped_text(pdf, f"MFD      :  {mfd}", x=x1, y=y5_1, font=font, size=size, max_width=max_text_width)

    medium_size = 6
    # ADD CUSTOMER CARE ADDRESS LABEL
    y8 = y5_1 - 3 * mm
    add_wrapped_text(pdf, "Customer Care Address & Mfd For:", x=x1, y=y8, font=font_a, size=medium_size, max_width=max_text_width)

    small_size = 5
    # ADD CUSTOMER CARE ADDRESS TEXT
    y9 = y8 - 2 * mm
    add_wrapped_text(pdf, "Mahavir Home Appliances, 137/2, 1st Main, 3rd Cross, New Timber Yard Layout Mysore Road, Bangalore-560026", x=x1, y=y9, font=font, size=small_size, max_width=max_text_width)

    small_size = 5

    # ADD TOLL FREE NUMBER
    y11 = draw_labeled_text_with_fit(pdf, 
                                    label="Toll Free No.: ", 
                                    text="08061977979, 18001026019", 
                                    x=x1, 
                                    y=y9 - (small_size + 16),
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=6, 
                                    text_size=5, 
                                    max_width=max_text_width)

    # ADD EMAIL ADDRESS
    address_font_size_u = 12
    y12 = draw_labeled_text_with_fit(pdf, 
                                    label="Email Id: ", 
                                    text="customercare@rallyappliances.com", 
                                    x=x1, 
                                    y=y11 + 2,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=6, 
                                    text_size=5, 
                                    max_width=max_text_width)

    # ADD TIMINGS
    y13 = draw_labeled_text_with_fit(pdf, 
                                    label="Timing: ", 
                                    text="10:30am to 5:00pm(Sunday Holiday)", 
                                    x=x1, 
                                    y=y12 + 2,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=6, 
                                    text_size=5, 
                                    max_width=max_text_width)

    small_size = 5
    # ADD MANUFACTURE LOCATION
    y10 = draw_labeled_text_with_wrap(pdf, 
                                    label="Mfd at: ", 
                                    text=mfd_at, 
                                    x=x1, 
                                    y=y13 + 2,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=6, 
                                    text_size=5, 
                                    max_width=max_text_width)

    # ADD IMAGE TO PDF
    add_image(pdf, image_path, x=border_inset + 37 * mm, y=border_inset + 31 * mm, width=10 * mm, height=10 * mm)
    
    # SAVE THE PDF
    pdf.save()

    buffer.seek(0)
    return buffer

import io
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont

from utils import fit_text_in_box, fit_text_in_box_centered, add_wrapped_text, add_line, add_image, draw_labeled_text_with_fit, draw_labeled_text_with_wrap

# REGISTER CUSTOM FONTS
pdfmetrics.registerFont(TTFont('Monstera_Bold', 'Monstera_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Monstera_Thin', 'Monstera_Thin.ttf'))

def universal_mrp_sticker_unites(category, model, content, mrp, mfd, mfd_at):
    # DEFINE PDF DIMENSIONS
    width, height = 150 * mm, 100 * mm # SET LANDSCAPE DIMENSIONS
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    # DEFINE BORDER DIMENSIONS
    border_inset = 2 * mm
    border_width = width - 2 * border_inset
    border_height = height - 2 * border_inset
    pdf.rect(border_inset, border_inset, border_width, border_height)

    # SET FONTS AND SIZES
    font_a = "Monstera_Bold"
    font = "Monstera_Thin"
    size = 14
    text_margin = 3 * mm
    max_text_width = border_width - 2 * text_margin

    # INITIAL TEXT POSITIONING
    x1 = border_inset + text_margin
    y1 = height - 8 * mm
    

    # ADD CONTENT TEXT
    fit_text_in_box(pdf, f"Content              :  {content} UNITS OF {category}", x1, y1, font, 16, max_text_width)
    
    # ADD MODEL TEXT
    y1_yy = y1 - (12 + 8)
    fit_text_in_box(pdf, f"Model                  :  {model}", x1, y1_yy, font, 16, max_text_width)

    # ADD MRP TEXT
    y2 = y1_yy - (size + 8)
    fit_text_in_box(pdf, f"MRP for 1 Unit     :   ₹ {mrp}.00/- (Incl of All Taxes)", x1, y2, font_a, 16, max_text_width)
    
    size_y2 = 12
    y2_1 = y2 - (size_y2 + 8)
    mrp_numeric = mrp.replace(',', '')
    
    try:
        total_mrp = int(mrp_numeric) * int(content)
    except ValueError:
        total_mrp = 0

    formatted_mrp = f"{total_mrp:,}"
    fit_text_in_box(pdf, f"MRP for {content} units  :   ₹ {formatted_mrp}.00/- (Incl of All Taxes)", x1, y2_1, font_a, 16, max_text_width)

    # ADD MANUFACTURE DATE TEXT
    y3 = y2_1 - (size + 7)
    fit_text_in_box(pdf, f"Month of MFD      :    {mfd}", x1, y3, font, 16, max_text_width)

    # ADD CUSTOMER CARE ADDRESS LABEL
    small_font_size = 12
    y4 = draw_labeled_text_with_fit(pdf, 
                                    label="Customer Care Address & Mktd by: ", 
                                    text="Mahavir Home Appliances", 
                                    x=x1, 
                                    y=y3 - (size + 8),
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=12, 
                                    text_size=11, 
                                    max_width=max_text_width)

    # ADD ADDRESS TEXT
    address_font_size = 12
    y5 = y4
    add_wrapped_text(pdf, "#137/2, 1st Main, 3rd Cross New Timberyard Layout Mysore Road, Bangalore - 560026", x=x1, y=y5, font=font, size=address_font_size, max_width=max_text_width)

    # ADD SERVICE CONTACT LABEL
    y6 = y5 - (address_font_size + 18)
    add_wrapped_text(pdf, "For Service Contact:", x=x1, y=y6, font=font, size=address_font_size, max_width=max_text_width)

    # ADD TOLL FREE NUMBER
    y7 = draw_labeled_text_with_fit(pdf, 
                                    label="Toll Free No.: ", 
                                    text="08061977979, 18001026019", 
                                    x=x1, 
                                    y=y6 - (small_font_size + 4),
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=12, 
                                    text_size=11, 
                                    max_width=max_text_width)

    # ADD EMAIL ADDRESS
    address_font_size_u = 12
    y8 = draw_labeled_text_with_fit(pdf, 
                                    label="Email Id: ", 
                                    text="customercare@rallyappliances.com", 
                                    x=x1, 
                                    y=y7 - 1,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=12, 
                                    text_size=11, 
                                    max_width=max_text_width)

    # ADD TIMINGS
    y9 = draw_labeled_text_with_fit(pdf, 
                                    label="Timing: ", 
                                    text="10:30am to 5:00pm(Sunday Holiday)", 
                                    x=x1, 
                                    y=y8 - 1,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=12, 
                                    text_size=11, 
                                    max_width=max_text_width)

    # ADD MANUFACTURE LOCATION
    y10 = draw_labeled_text_with_wrap(pdf, 
                                    label="Mfd at: ", 
                                    text=mfd_at, 
                                    x=x1, 
                                    y=y9 - 1,
                                    font_label=font_a, 
                                    font_text=font, 
                                    label_size=12, 
                                    text_size=11, 
                                    max_width=max_text_width)

    # ADD HORIZONTAL LINES FOR SEPARATION
    add_line(pdf, border_inset, y1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y3 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y1_yy - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2_1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2 - 2 * mm, width - border_inset)

    # DEFINE BOX DIMENSIONS
    box_x = 104 * mm
    box_y = 25 * mm
    box_width = 44 * mm
    box_height = 22 * mm

    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.rect(box_x, box_y, box_width, box_height, fill=0)

    box_text = f"{category}"
    fit_text_in_box_centered(pdf, box_text, box_x, box_y + 14 * mm, font, 18, box_width)
    
    box_text = f"{model}"
    fit_text_in_box_centered(pdf, box_text, box_x, box_y + 4 * mm, font, 18, box_width)

    # SAVE THE PDF TO BUFFER
    pdf.save()

    buffer.seek(0)
    return buffer

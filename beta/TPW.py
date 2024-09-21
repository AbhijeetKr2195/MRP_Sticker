from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io

pdfmetrics.registerFont(TTFont('Monstera', 'Monstera.ttf'))

def generate_mrp_sticker(category, model, content, mrp, mfd, mfd_at, image_path):
    category = category.upper()
    model = model.upper()
    content = content.upper()
    mfd = mfd.upper()
    mfd_at = mfd_at.upper()

    width, height = 100 * mm, 75 * mm
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    border_inset = 3 * mm
    border_width = width - 2 * border_inset
    border_height = height - 2 * border_inset

    # Draw border
    pdf.rect(border_inset, border_inset, border_width, border_height)

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
            y -= size + 2  # Move down for the next line, adjust 2 for spacing

    def add_line(pdf, x, y, end_x):
        pdf.line(x, y, end_x, y)

    def add_image(pdf, image_path, x, y, width, height):
        try:
            img = ImageReader(image_path)
            pdf.drawImage(img, x, y, width=width, height=height)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")

    font = "Monstera"
    size = 10
    text_margin = 5 * mm
    max_text_width = border_width - 2 * text_margin

    x1 = border_inset + text_margin  # 5 mm from the left border
    y1 = height - 8 * mm  # Start from 8 mm from the top

    if content.isdigit() and int(content) == 1:
        content_t = f"{content} Unit of {category}"
    else:
        content_t = f"{content} Units of {category}"

    add_wrapped_text(pdf, f"Content: {content_t} ", x=x1, y=y1, font=font, size=size, max_width=max_text_width)
    y2 = y1 - (size + 8)  # Adjust for the next block of text
    add_wrapped_text(pdf, f"MRP: ₹ {mrp}.00/- (Incl of All Taxes)", x=x1, y=y2, font=font, size=size, max_width=max_text_width)
    y3 = y2 - (size + 8)
    add_wrapped_text(pdf, f"Month of MFD: {mfd}", x=x1, y=y3, font=font, size=size, max_width=max_text_width)

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

    address_font_size_r = 8
    y8 = y7 - (address_font_size_r + 4)
    add_wrapped_text(pdf, "Email Id: customercare@rallyappliances.com", x=x1, y=y8, font=font, size=address_font_size_r, max_width=max_text_width)

    y9 = y8 - (small_font_size + 4)
    add_wrapped_text(pdf, "Timing: 10:30am to 5:00pm(Sunday Holiday)", x=x1, y=y9, font=font, size=small_font_size, max_width=max_text_width)

    y10 = y9 - (address_font_size + 4)
    add_wrapped_text(pdf, f"Mfd at: {mfd_at}", x=x1, y=y10, font=font, size=address_font_size, max_width=max_text_width)

    y11 = y10 - (address_font_size + 20)
    add_wrapped_text(pdf, f"{category} - {model}    ₹ {mrp}.00/-", x=x1, y=y11, font=font, size=address_font_size, max_width=max_text_width)

    # Draw lines
    add_line(pdf, border_inset, y1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y3 - 2 * mm, width - border_inset)

    # Add image
    image_width = 17 * mm  
    image_height = 16 * mm  
    x_image = border_inset + 75 * mm  
    y_image = border_inset + 23 * mm  
    add_image(pdf, image_path, x_image, y_image, image_width, image_height)

    # Finalize the PDF
    pdf.save()

    # Move the buffer position to the beginning
    buffer.seek(0)
    return buffer

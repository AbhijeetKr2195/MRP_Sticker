from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import os

pdfmetrics.registerFont(TTFont('Monstera', 'Monstera.ttf'))

def ceiling_U_mrp_sticker(category, model, content, mrp, mfd, mfd_at, image_path, image_path1):
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
        if os.path.exists(image_path):
            try:
                img = ImageReader(image_path)
                pdf.drawImage(img, x, y, width, height)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
        else:
            print(f"Image not found: {image_path}")

    width, height = 100 * mm, 75 * mm
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    border_inset = 3 * mm
    border_width = width - 2 * border_inset
    border_height = height - 2 * border_inset

    # Draw border
    pdf.rect(border_inset, border_inset, border_width, border_height)

    font = "Monstera"
    size = 10
    text_margin = 5 * mm
    max_text_width = border_width - 2 * text_margin

    x1 = border_inset + 3 * mm  # 3 mm from the left border
    y1 = height - 7 * mm  # Start from 7 mm from the top

    add_wrapped_text(pdf, f"ITEM:    {model}", x=x1, y=y1, font=font, size=size, max_width=max_text_width)

    size_a = 6
    y2 = y1 - (size_a + 8)  # Adjust for the next block of text
    add_wrapped_text(pdf, "220-240 Volts, 50/60 Hz", x=x1, y=y2, font=font, size=size_a, max_width=max_text_width)

    y3 = y2 - (size + 6)

    add_wrapped_text(pdf, f"Content: {content} Units of {category}", x=x1, y=y3, font=font, size=size, max_width=max_text_width)

    small_font_size = 8
    y4 = y3 - (small_font_size + 6)
    add_wrapped_text(pdf, f"MRP Per Unit:    ₹ {mrp}", x=x1, y=y4, font=font, size=small_font_size, max_width=max_text_width)

    small_font_size_a = 6
    y4_1 = y4 - (small_font_size_a + 3)
    mrp = mrp.replace(',', '')  # Remove commas for calculation
    total_mrp = int(mrp) * int(content)  # Calculate total without changing content

    # Format total_mrp with commas for display
    formatted_mrp = f"{total_mrp:,}"

    add_wrapped_text(pdf, f"MRP of {content} units:   ₹ {formatted_mrp}", x=x1, y=y4_1, font=font, size=small_font_size_a, max_width=max_text_width)

    address_font_size = 7
    y5 = y4_1 - (small_font_size + 3)
    add_wrapped_text(pdf, "(Inclusive Of All Taxes)", x=x1, y=y5, font=font, size=small_font_size, max_width=max_text_width)

    y6 = y5 - (size + 8)
    add_wrapped_text(pdf, f"Date Of MFD:    {mfd}", x=x1, y=y6, font=font, size=size, max_width=max_text_width)

    y7 = y6 - (address_font_size + 7)
    add_wrapped_text(pdf, "Customer Care Address & Mkd By: Mahavir Home Appliances", x=x1, y=y7, font=font, size=address_font_size, max_width=max_text_width)

    y8 = y7 - (address_font_size + 4)
    add_wrapped_text(pdf, "#137/2, 1st Main, 3rd Cross New Timberyard Layout Mysore Road, Bangalore - 560026", x=x1, y=y8, font=font, size=address_font_size, max_width=max_text_width)

    small_font_size = 6
    y9 = y8 - (small_font_size + 14)
    add_wrapped_text(pdf, f"Mfd at: {mfd_at}", x=x1, y=y9, font=font, size=small_font_size, max_width=max_text_width)

    address_font_size = 9
    y10 = y9 - (address_font_size + 12)
    add_wrapped_text(pdf, "E-mail: customercare@rallyappliances.com", x=x1, y=y10, font=font, size=address_font_size, max_width=max_text_width)

    y11 = y10 - (address_font_size + 5)
    add_wrapped_text(pdf, "Toll Free No.: 08061977979 | 18001026019", x=x1, y=y11, font=font, size=address_font_size, max_width=max_text_width)

    y12 = y11 - (address_font_size + 4)
    add_wrapped_text(pdf, "Timings: 10:30 AM to 5:00 PM (Sunday Holiday)", x=x1, y=y12, font=font, size=address_font_size, max_width=max_text_width)

    # Add lines
    add_line(pdf, border_inset, y1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y3 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y5 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y6 - 2 * mm, width - border_inset)

    # Add images
    add_image(pdf, image_path, x=border_inset + 78 * mm, y=border_inset + 42 * mm, width=10 * mm, height=10 * mm)
    add_image(pdf, image_path1, x=border_inset + 81 * mm, y=border_inset + 23 * mm, width=12 * mm, height=6 * mm)

    # Finalize the PDF
    pdf.save()


    # Move the buffer position to the beginning
    buffer.seek(0)
    return buffer

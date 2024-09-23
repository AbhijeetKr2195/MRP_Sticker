from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io

pdfmetrics.registerFont(TTFont('Monstera', 'Monstera.ttf'))

def generate_U_mrp_sticker(category, model, content, mrp, mfd, mfd_at, image_path1="a.png"):
    category = category.upper()
    model = model.upper()
    content = content.upper()
    mfd = mfd.upper()
    mfd_at = mfd_at.upper()

    # Adjusted page height to accommodate y = 105 mm + box height = 20 mm
    width, height = 151 * mm, 101 * mm  # Increased height from 101 mm to 130 mm
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
    size = 12
    text_margin = 5 * mm
    max_text_width = border_width - 2 * text_margin

    x1 = border_inset + text_margin  # 5 mm from the left border
    y1 = height - 8 * mm  # Start from 8 mm from the top

    add_wrapped_text(pdf, f"MODEL :    {category} - {model}", x=x1, y=y1, font=font, size=size, max_width=max_text_width)
    # Existing MRP text
    y2 = y1 - (size + 8)
    add_wrapped_text(pdf, f"MRP for 1 Unit :    ₹ {mrp}.00/- (Incl of All Taxes)", x=x1, y=y2, font=font, size=size, max_width=max_text_width)

    size_y2 = 12
    y2_1 = y2 - (size_y2 + 8)
    mrp_numeric = mrp.replace(',', '')  # Remove commas for calculation
    try:
        total_mrp = int(mrp_numeric) * int(content)  # Calculate total without changing content
    except ValueError:
        total_mrp = 0  # Handle cases where conversion fails

    # Format total_mrp with commas for display
    formatted_mrp = f"{total_mrp:,}"

    add_wrapped_text(pdf, f"MRP for {content} units :   ₹ {formatted_mrp}.00/- (Incl of All Taxes)", x=x1, y=y2_1, font=font, size=size_y2, max_width=max_text_width)

    # Continue with the next block of text
    y3 = y2_1 - (size + 7)
    add_wrapped_text(pdf, f"Month of MFD :    {mfd}", x=x1, y=y3, font=font, size=size, max_width=max_text_width)

    small_font_size = 12
    y4 = y3 - (small_font_size + 10)
    add_wrapped_text(pdf, "Customer Care Address & Mktd by: Mahavir Home Appliances", x=x1, y=y4, font=font, size=small_font_size, max_width=max_text_width)

    address_font_size = 12
    y5 = y4 - (address_font_size + 16)
    add_wrapped_text(pdf, "#137/2, 1st Main, 3rd Cross New Timberyard Layout Mysore Road, Bangalore - 560026", x=x1, y=y5, font=font, size=address_font_size, max_width=max_text_width)

    y6 = y5 - (address_font_size + 18)
    add_wrapped_text(pdf, "For Service Contact:", x=x1, y=y6, font=font, size=address_font_size, max_width=max_text_width)

    y7 = y6 - (address_font_size + 4)
    add_wrapped_text(pdf, "Toll Free No.: 080-61977979, 18001026019", x=x1, y=y7, font=font, size=address_font_size, max_width=max_text_width)

    address_font_size_u = 12
    y8 = y7 - (address_font_size_u + 6)
    add_wrapped_text(pdf, "Email Id: customercare@rallyappliances.com", x=x1, y=y8, font=font, size=address_font_size_u, max_width=max_text_width)

    y9 = y8 - (small_font_size + 6)
    add_wrapped_text(pdf, "Timing: 10:30am to 5:00pm(Sunday Holiday)", x=x1, y=y9, font=font, size=small_font_size, max_width=max_text_width)

    y10 = y9 - (address_font_size + 10)
    add_wrapped_text(pdf, "Mfd at: M/s. Rally International", x=x1, y=y10, font=font, size=address_font_size, max_width=max_text_width)

    y11 = y10 - (address_font_size + 10)
    add_wrapped_text(pdf, f"{mfd_at.title()}", x=x1, y=y11, font=font, size=address_font_size, max_width=max_text_width)

    # Draw lines
    add_line(pdf, border_inset, y1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y3 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2_1 - 2 * mm, width - border_inset)
    add_line(pdf, border_inset, y2 - 2 * mm, width - border_inset)

    # Add image
    image_width = 19 * mm  
    image_height = 9 * mm  
    x_image = border_inset + 122 * mm  
    y_image = border_inset + 21 * mm  
    add_image(pdf, image_path1, x_image, y_image, image_width, image_height)

    # Add the 39mm x 20mm box at (75mm, 105mm)
    box_x = 109 * mm
    box_y = 34 * mm
    box_width = 39 * mm
    box_height = 18 * mm

    # Optional: Customize the box appearance
    pdf.setStrokeColorRGB(0, 0, 0)  # Black border
    pdf.setFillColorRGB(0, 0, 0)    # White fill (optional)
    pdf.rect(box_x, box_y, box_width, box_height, fill=0)  # Set fill=1 if you want to fill the box

    # If you want to add text inside the box, you can do so as follows:
    # Example:
    box_text = f"{category}"
    pdf.setFont(font, 18)
    text_width = pdf.stringWidth(box_text, font, 18)
    text_x = box_x + (box_width - text_width) / 2
    text_y = box_y + 12 * mm
    pdf.drawString(text_x, text_y, box_text)

    box_text = f"{model}"
    pdf.setFont(font, 18)
    text_width = pdf.stringWidth(box_text, font, 18)
    text_x = box_x + (box_width - text_width) / 2
    text_y = box_y + 4 * mm
    pdf.drawString(text_x, text_y, box_text)

    # Finalize the PDF
    pdf.save()

    # Move the buffer position to the beginning
    buffer.seek(0)
    return buffer


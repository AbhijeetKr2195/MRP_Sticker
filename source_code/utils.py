import os
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

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

    # DRAW EACH LINE OF WRAPPED TEXT
    for line in lines:
        pdf.drawString(x, y, line)
        y -= size + 2

# FUNCTION TO ADD A LINE TO THE PDF
def add_line(pdf, x, y, end_x):
    pdf.line(x, y, end_x, y)

# FUNCTION TO ADD AN IMAGE TO THE PDF
def add_image(pdf, image_path, x, y, width, height):
    if os.path.exists(image_path):
        try:
            img = ImageReader(image_path)
            pdf.drawImage(img, x, y, width, height)
        except Exception as e:
            print(f"ERROR LOADING IMAGE {image_path}: {e}")
    else:
        print(f"IMAGE NOT FOUND: {image_path}")

# FUNCTION TO FIT TEXT WITHIN A SPECIFIED BOX
def fit_text_in_box(pdf, text, x, y, font, initial_size, box_width):
    # FUNCTION TO CALCULATE THE MAXIMUM FONT SIZE THAT FITS IN THE WIDTH
    def calculate_fitting_size(text, font, size, max_width):
        while pdf.stringWidth(text, font, size) > max_width and size > 1:
            size -= 0.5
        return size

    fitting_size = calculate_fitting_size(text, font, initial_size, box_width)
    pdf.setFont(font, fitting_size)

    text_width = pdf.stringWidth(text, font, fitting_size)
    text_x = x
    pdf.drawString(text_x, y, text)

# FUNCTION TO FIT TEXT IN CENTERED BOX
def fit_text_in_box_centered(pdf, text, x, y, font, initial_size, box_width):
    # FUNCTION TO CALCULATE THE MAXIMUM FONT SIZE THAT FITS IN THE WIDTH
    def calculate_fitting_size(text, font, size, max_width):
        while pdf.stringWidth(text, font, size) > max_width and size > 1:
            size -= 0.5
        return size

    fitting_size = calculate_fitting_size(text, font, initial_size, box_width)
    pdf.setFont(font, fitting_size)

    text_width = pdf.stringWidth(text, font, fitting_size)
    text_x = x + (box_width - text_width) / 2
    pdf.drawString(text_x, y, text)

# FUNCTION TO DRAW LABELED TEXT WITH FITTED TEXT
def draw_labeled_text_with_fit(pdf, label, text, x, y, font_label, font_text, label_size, text_size, max_width):
    pdf.setFont(font_label, label_size)
    label_width = pdf.stringWidth(label, font_label, label_size)
    pdf.drawString(x, y, label)
    
    new_x_position = x + label_width
    remaining_width = max_width - label_width
    fit_text_in_box(pdf, text, new_x_position, y, font_text, text_size, remaining_width)

    return y - (text_size + 4)

# FUNCTION TO DRAW LABELED TEXT WITH WRAPPING
def draw_labeled_text_with_wrap(pdf, label, text, x, y, font_label, font_text, label_size, text_size, max_width):
    pdf.setFont(font_label, label_size)
    label_width = pdf.stringWidth(label, font_label, label_size)
    pdf.drawString(x, y, label)
    
    new_x_position = x + label_width
    remaining_width = max_width - label_width
    add_wrapped_text(pdf, text, x=new_x_position, y=y, font=font_text, size=text_size, max_width=remaining_width)

    return y - (text_size + 4)

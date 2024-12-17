import pytesseract
from PIL import Image
import cv2
import os
import re
from datetime import datetime

# Paths
image_path = "Project1/test-files/jpg_image1.jpg"
temp_image_folder = "Project1/temp"
ocr_result_folder = "Project1/ocr_result"
ocr_result_file = os.path.join(ocr_result_folder, "extracted_text.txt")

company_name = "N/A"
user_name = "N/A"
total_amount = "N/A"
expense_date = "N/A"
mode_of_travel = "N/A"

# Ensure the folders exist 
os.makedirs(temp_image_folder, exist_ok=True)
os.makedirs(ocr_result_folder, exist_ok=True)

# Load and resize image
image = cv2.imread(image_path)
im = Image.open(image_path)
new_image = im.resize((1226, 1740))
new_image_path = os.path.join(temp_image_folder, "resized_image.jpg")
new_image.save(new_image_path)
resized_image = cv2.imread(new_image_path)

# Extract initial text using pytesseract (without omit areas)
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray)

# Check if the text contains the word "OLA" or "Ola"
if "OLA" in text or "Ola" in text:
    # Define omit areas and draw white rectangles over them if it's an OLA image
    omit_area = (120, 400, 550, 1000)
    omit_area2 = (600, 980, 1050, 1100)

    x1, y1, x2, y2 = omit_area
    cv2.rectangle(resized_image, (x1, y1), (x2, y2), (255, 255, 255), -1)

    x3, y3, x4, y4 = omit_area2
    cv2.rectangle(resized_image, (x3, y3), (x4, y4), (255, 255, 255), -1)

    # Convert to grayscale and reprocess the image
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

# Save the processed grayscale image
gray_image_path = os.path.join(temp_image_folder, "index_gray.jpg")
cv2.imwrite(gray_image_path, gray)

# Print the extracted text to the console
print("Extracted Text:")
print(text)

# Write the extracted text to a new text file
with open(ocr_result_file, "w") as file:
    file.write(text)

# Function to format the date
def format_date(date_str):
    try:
        # Convert to datetime object
        date_obj = datetime.strptime(date_str, '%d %b, %Y')
        # Format as "day month_name year"
        formatted_date = date_obj.strftime('%d %B %Y')
        return formatted_date
    except ValueError:
        return "N/A"

# Proceed with extraction if OLA or Ola was found in the text
if "OLA" in text or "Ola" in text:
    company_name = "OLA"
    lines = text.splitlines()

    # Find the line with the 13-character long Invoice Serial ID
    invoice_number_line = None
    for i, line in enumerate(lines):
        if "Invoice Serial Id:" in line:
            invoice_number_line = i
            break
    
    # Extract the total amount from the line after the invoice serial ID
    total_amount = "N/A"
    if invoice_number_line is not None:
        next_line = lines[invoice_number_line + 1].strip()
        if not next_line:  # If the next line is empty, check the following line
            next_line = lines[invoice_number_line + 2].strip()

        # Extract the numeric value from the identified line
        total_amount = re.sub(r'[^\d]', '', next_line)

    # Regex patterns for other information
    user_pattern = r"Thanks for travelling with us, (.+)"
    expense_date_pattern = r"(\d{1,2} [A-Za-z]+, \d{4})"
    invoice_number_pattern = r"Invoice Serial Id:(\w+)"
    mode_of_travel_pattern = r"(Auto\s*-\s*[A-Za-z-]+|Cab)"

    # Find matches
    user_match = re.search(user_pattern, text)
    expense_date_match = re.search(expense_date_pattern, text)
    invoice_number_match = re.search(invoice_number_pattern, text)
    mode_of_travel_match = re.search(mode_of_travel_pattern, text)

    # Extract values
    user_name = user_match.group(1) if user_match else "N/A"
    expense_date = format_date(expense_date_match.group(1)) if expense_date_match else "N/A"
    invoice_number = invoice_number_match.group(1) if invoice_number_match else "N/A"
    mode_of_travel = mode_of_travel_match.group(1).strip() if mode_of_travel_match else "Cab"

    # Print extracted information
    print("\nExtracted Information:")
    print(f"Company Name: {company_name}")
    print(f"User Name: {user_name}")
    print(f"Total Amount: ₹{total_amount}")
    print(f"Expense Date: {expense_date}")
    print(f"Invoice Number: {invoice_number}")
    print(f"Mode of Travel: {mode_of_travel}")

    # Save the extracted information to a text file
    extracted_info_file = os.path.join(ocr_result_folder, "extracted_info.txt")
    with open(extracted_info_file, "w") as file:
        file.write(f"Company Name: {company_name}\n")
        file.write(f"User Name: {user_name}\n")
        file.write(f"Total Amount: ₹{total_amount}\n")
        file.write(f"Expense Date: {expense_date}\n")
        file.write(f"Invoice Number: {invoice_number}\n")
        file.write(f"Mode of Travel: {mode_of_travel}\n")

# Check if the text contains the word "Uber"
elif "Uber" in text:
    company_name = "Uber"
    lines = text.splitlines()
    
    for line in lines:
        if "Uber" in line:
            # Regex pattern to match the date format "Month day, year" after "Uber"
            date_match = re.search(r"Uber\s+([A-Za-z]+\s\d{1,2},\s\d{4})", line)
            if date_match:
                expense_date = format_date(date_match.group(1))
            break

    user_pattern = r"Here's your receipt for your ride, (.+)"
    total_amount_pattern = r"Total\s*%?\s*([\d,\.]+)"
    mode_of_travel_pattern = r"Uber (Auto|Cab)"
    
    user_match = re.search(user_pattern, text)
    total_amount_match = re.search(total_amount_pattern, text)
    mode_of_travel_match = re.search(mode_of_travel_pattern, text)

    user_name = user_match.group(1) if user_match else "N/A"
    total_amount = total_amount_match.group(1) if total_amount_match else "N/A"
    mode_of_travel = mode_of_travel_match.group(1).strip() if mode_of_travel_match else "Cab"

    # Print extracted information
    print("\nExtracted Information:")
    print(f"Company Name: {company_name}")
    print(f"User Name: {user_name}")
    print(f"Total Amount: ₹{total_amount}")
    print(f"Expense Date: {expense_date}")
    print(f"Mode of Travel: {mode_of_travel}")

    # Save the extracted information to a text file
    extracted_info_file = os.path.join(ocr_result_folder, "extracted_info.txt")
    with open(extracted_info_file, "w") as file:
        file.write(f"Company Name: {company_name}\n")
        file.write(f"User Name: {user_name}\n")
        file.write(f"Total Amount: ₹{total_amount}\n")
        file.write(f"Expense Date: {expense_date}\n")
        file.write(f"Mode of Travel: {mode_of_travel}\n")

else:
    print("The text does not contain the word 'OLA' or 'Uber'.")

# Display the processed image
cv2.imshow('Processed Image', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

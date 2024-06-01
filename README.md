## README.md

```markdown
# HTML Parser to CSV Converter

This project is a GUI application built using Python's Tkinter library that parses HTML files to extract product data and saves it to a CSV file. It is designed to extract specific information from Amazon-like HTML pages, such as product links, titles, ratings, prices, and last month sold data.

## Features

- Select an HTML file and parse its content.
- Extract product information such as links, titles, ratings, prices, and last month sold data.
- Save the extracted data to a CSV file.
- Simple and user-friendly graphical interface.

## Requirements

- Python 3.x
- Tkinter
- BeautifulSoup4
- pandas
- PIL (Pillow)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mushafkhan7/html-parser-to-csv.git
   cd html-parser-to-csv
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Place your `logo.png` file in the project directory.

## Usage

1. Run the application:
   ```sh
   python app.py
   ```

2. Click the "Select HTML File" button to choose an HTML file.
3. After selecting the file, the application will parse it and prompt you to save the extracted data as a CSV file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

## requirements.txt

```plaintext
tk
beautifulsoup4
pandas
Pillow
```

## LICENSE

```plaintext
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## app.py

Add comments to your `app.py` for better understanding:

```python
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from PIL import Image, ImageTk

def parse_html_file(file_path):
    """
    Parses the HTML file to extract product data.

    Args:
        file_path (str): The path to the HTML file.

    Returns:
        dict: A dictionary containing extracted product data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all('div', class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20 gsx-ies-anchor")

    data = {
        'link': [],
        'title': [],
        'rating': [],
        'price': [],
        'last_month_sold': []
    }

    base_url = 'https://m.media-amazon.com/images/'

    for div in divs:
        link = ''
        title = ''
        rating = ''
        price = ''
        last_month_sold = ''

        # Extract image link
        img = div.find('img', class_="s-image s-image-optimized-rendering")
        if img and 'src' in img.attrs:
            img_src = img['src']
            if not img_src.startswith('http'):
                link = urljoin(base_url, img_src)
            else:
                link = img_src

        # Extract title
        title_span = div.find('span', class_="a-size-base-plus a-color-base a-text-normal")
        if title_span:
            title = title_span.get_text(strip=True)

        # Extract rating
        rating_span = div.find('span', class_="a-icon-alt")
        if rating_span:
            rating = rating_span.get_text(strip=True)

        # Extract price
        price_span = div.find('span', class_='a-price-whole')
        if price_span:
            price = price_span.get_text(strip=True)

        # Extract last month sold data
        last_month_sold_span = div.find('span', class_='a-size-base a-color-secondary')
        if last_month_sold_span:
            last_month_sold = last_month_sold_span.get_text(strip=True)

        data['link'].append(link)
        data['title'].append(title)
        data['rating'].append(rating)
        data['price'].append(price)
        data['last_month_sold'].append(last_month_sold)

    return data

def save_to_csv(data, output_path):
    """
    Saves the extracted data to a CSV file.

    Args:
        data (dict): The data to save.
        output_path (str): The path to the output CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

def on_select_file():
    """
    Handles the file selection and data processing.
    """
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    if file_path:
        data = parse_html_file(file_path)
        output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if output_path:
            save_to_csv(data, output_path)
            messagebox.showinfo("Success", f"Data has been successfully saved to {output_path}")
        else:
            messagebox.showwarning("Save cancelled", "Save operation was cancelled.")
    else:
        messagebox.showwarning("File not selected", "No file was selected.")

# Set up the main application window
root = tk.Tk()
root.title("HTML Parser to CSV")
root.geometry("400x400")

# Load and resize the logo image
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((250, 150), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)

# Add the logo to a label widget
logo_label = tk.Label(root, image=logo)
logo_label.pack(pady=10)

# Add a button to trigger the file selection and processing
select_file_button = tk.Button(root, text="Select HTML File", command=on_select_file, padx=20, pady=10)
select_file_button.pack(pady=20)

# Run the application
root.mainloop()
```

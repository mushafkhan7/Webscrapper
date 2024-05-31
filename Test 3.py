import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from PIL import Image, ImageTk

def parse_html_file(file_path):
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

        img = div.find('img', class_="s-image s-image-optimized-rendering")
        if img and 'src' in img.attrs:
            img_src = img['src']
            if not img_src.startswith('http'):
                link = urljoin(base_url, img_src)
            else:
                link = img_src

        title_span = div.find('span', class_="a-size-base-plus a-color-base a-text-normal")
        if title_span:
            title = title_span.get_text(strip=True)

        rating_span = div.find('span', class_="a-icon-alt")
        if rating_span:
            rating = rating_span.get_text(strip=True)

        price_span = div.find('span', class_='a-price-whole')
        if price_span:
            price = price_span.get_text(strip=True)

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
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

def on_select_file():
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

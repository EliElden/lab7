import tkinter as tk
import requests
from io import BytesIO
from PIL import Image, ImageTk

def get_new_image():
    url = "https://nekos.best/api/v2/neko"
    response = requests.get(url)
    data = response.json()
      
    image_url = data["results"][0]["url"]
    
    img_response = requests.get(image_url)
    img_data = img_response.content
    
    image = Image.open(BytesIO(img_data))
    image = image.resize((400, 400), Image.Resampling.LANCZOS)
    
    tk_image = ImageTk.PhotoImage(image)
    image_label.config(image=tk_image)
    image_label.image = tk_image 

root = tk.Tk()
root.title("Генератор Неко-котиков")
root.geometry("450x500")

image_label = tk.Label(root)
image_label.pack(pady=10)

btn = tk.Button(root, text="Следующая картинка!", font=("Arial", 14), command=get_new_image)
btn.pack(pady=10)

get_new_image()

root.mainloop()
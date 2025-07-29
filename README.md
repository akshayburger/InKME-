# InkMe – Handwriting Generator 

**InkMe** is a handwriting generator that takes user-inputted text and converts it into realistic-looking handwritten images using your own sliced character images. Perfect for custom notes, digital letters, or fun image creation!

---

## 🚀 Features

* Upload your own handwriting (6×10 grid image)
* Automatically slice A–Z and a–z letters
* Type any text and get a handwriting-style image
* Customizable:

  * Font size
  * Line spacing
  * A4-sized page layout with auto-wrapping

* Download generated output as an image

---

## 📁 Project Structure
```InkMe/
├── main.py # Streamlit frontend
├── text_slicer.py # Slices character grid into individual images
├── converter.py # Converts typed text to handwritten-style image
├── output_letters/ # Contains sliced character images (char_00 to char_51)
│ ├── char_00.png
│ ├── ...
│ └── char_51.png
├── handwriting_grid.png # Your uploaded handwriting grid (6x10)
├── requirements.txt # Python dependencies
└── README.md
```


## BEFORE YOU EXECUTE!!


Type this in your terminal:



pip install -r requirements.txt



# IMPORTANT:
Make sure the handwriting grid image you upload is placed in the same directory as textˍ_slicer.py (i.e., inside the main InkMe folder).



## Run the file in the terminal!

python -m streamlit run main.py

## Example Working
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fce47b79-f8e5-4b8d-b4ba-718f0d29e3a8" />



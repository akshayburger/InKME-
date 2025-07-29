# InkMe – Handwriting Generator ✍️🖋️

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

InkMe/
├── main.py # Streamlit frontend
├── text\_slicer.py # Extracts character images from handwriting grid
├── converter.py # Converts text to stitched handwriting image
├── output\_letters/ # Folder where sliced characters are stored
├── requirements.txt # Python dependencies
└── README.md


## BEFORE YOU EXECUTE!!


Type this in your terminal:



pip install -r requirements.txt



# IMPORTANT:
Make sure the handwriting grid image you upload is placed in the same directory as slicer.py (i.e., inside the main InkMe folder).



## Run the file

streamlit run app.py


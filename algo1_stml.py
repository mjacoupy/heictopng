# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 17:51:11 2023

@author: m.jacoupy
"""

import streamlit as st
import os
from PIL import Image
import pillow_heif
import shutil
import tempfile
import zipfile

def convert_heic_to_png(uploaded_files):
    temp_dir = tempfile.mkdtemp()
    output_folder = os.path.join(temp_dir, 'JPG')
    os.makedirs(output_folder)

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        if file_name.lower().endswith('.heic'):
            heic_path = os.path.join(temp_dir, file_name)
            with open(heic_path, 'wb') as f:
                f.write(uploaded_file.getvalue())

            heif_file = pillow_heif.read_heif(heic_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            image_rgba = image.convert("RGBA")
            png_name = os.path.splitext(file_name)[0] + '.PNG'
            png_path = os.path.join(output_folder, png_name)
            image_rgba.save(png_path, "PNG")

            st.write(f"{file_name} a été converti en {png_name}")

    # Afficher les fichiers dans le dossier output_folder
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            st.write(os.path.join(root, file))

    return output_folder

def make_zip(source_folder, output_filename):
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_folder))

st.title("Convertisseur d'images HEIC en PNG")

uploaded_files = st.file_uploader("Glissez et déposez vos images HEIC ici", type=['heic'], accept_multiple_files=True)

if uploaded_files:
    if st.button("Convertir"):
        output_folder = convert_heic_to_png(uploaded_files)
        make_zip(output_folder, output_folder + ".zip")
        st.download_button("Télécharger les images converties", output_folder + ".zip", "images_converted.zip")

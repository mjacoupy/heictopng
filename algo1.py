import os
from PIL import Image
import pillow_heif

# Chemin du dossier contenant les images HEIC
input_folder = "C:/Users/m.jacoupy/Téléchargements/USA 2023 Dany/iphone/HEIC/"
# Chemin du sous-dossier où sauvegarder les images transformées en PNG
output_folder = os.path.join(input_folder, 'JPG/')

# Assurez-vous que le sous-dossier 'transformé' existe ou créez-le
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Parcourir tous les fichiers du dossier HEIC
for file_name in os.listdir(input_folder):
    # Si le fichier est une image HEIC
    if file_name.lower().endswith('.heic'):
        heic_path = os.path.join(input_folder, file_name)
        # Lecture du fichier HEIC
        heif_file = pillow_heif.read_heif(heic_path)

        # Convertir HEIC en image PIL
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        # Convertir l'image en mode RGBA pour la transparence
        image_rgba = image.convert("RGBA")

        # Définir le chemin de sortie pour le fichier PNG
        png_name = os.path.splitext(file_name)[0] + '.PNG'
        png_path = os.path.join(output_folder, png_name)

        # Sauvegarder l'image au format PNG
        image_rgba.save(png_path, "PNG")

        print(f"{heic_path} a été converti et pivoté pour devenir {png_path}")

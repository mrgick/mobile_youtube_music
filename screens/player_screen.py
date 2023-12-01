from kivymd.uix.screen import MDScreen

class PlayerScreen(MDScreen):
    pass


# import io
# from kivy.uix.image import Image
# from kivy.core.image import Image as CoreImage
# import requests

# def get_kivy_image_from_bytes(image_bytes, file_extension):
#     # Return a Kivy image set from a bytes variable
#     buf = io.BytesIO(image_bytes)
#     cim = CoreImage(buf, ext=file_extension)
#     return Image(texture=cim.texture)

# # Example
# url = 'https://i.pinimg.com/564x/2a/3b/17/2a3b175c8b6752a62a6f6915ff472f8c.jpg'
# bimage = requests.get(url).content
# ext = 'jpg'
# image = get_kivy_image_from_bytes(bimage, ext)

# # https://stackoverflow.com/questions/63875884/set-a-kivy-image-from-a-bytes-variable
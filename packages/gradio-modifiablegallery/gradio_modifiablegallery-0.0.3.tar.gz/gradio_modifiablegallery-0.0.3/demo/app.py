from pathlib import Path

import gradio as gr
from gradio_modifiablegallery import ModifiableGallery

example = ModifiableGallery().example_value()


def delete_image(current_images, event: gr.EventData):

    image_to_delete_name = Path(event._data).name

    new_images = []
    for image, caption in current_images:
        if Path(image).name != image_to_delete_name:
            new_images.append((image, caption))

    return new_images


img = ("/home/ubuntu/gen-design-interface/tmp.jpg", "")
with gr.Blocks() as demo:
    with gr.Row():
        ModifiableGallery(label="Blank")  # blank component
        gallery = ModifiableGallery(
            value=[img, img, img], label="Populated", deletable=True
        )
        gallery.delete_image(fn=delete_image, inputs=gallery, outputs=gallery)


if __name__ == "__main__":
    demo.launch()

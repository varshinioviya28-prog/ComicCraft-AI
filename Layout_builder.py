def build_comic_layout(images, stories):
    layout = []
    for img, text in zip(images, stories):
        layout.append({"image": img, "text": text})
    return layout

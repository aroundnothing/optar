import picture


f = "Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut pharetra lacinia " \
    "libero, eget placerat ante rutrum non. Morbi dapibus id leo nec pulvinar. Nulla et metus a ipsum pellentesque " \
    "euismod. Fusce ut fermentum nisi, vitae vehicula purus. Ut eu tincidunt risus. Cras condimentum varius orci in " \
    "tempor. Etiam blandit, purus et aliquam lobortis, ante ipsum varius mi, eu accumsan urna tellus in neque. Maecenas" \
    " in neque augue. Donec mi arcu, pretium ac diam et, rutrum porta magna. Ut hendrerit eros ut tellus vehicula, " \
    "vitae tempus justo volutpat. Nulla tincidunt tortor vel ex malesuada, sit amet euismod ligula pretium. Vestibulum " \
    "tempor ligula eget lectus eleifend, in suscipit mauris varius. In finibus suscipit dolor, sit amet dignissim dui " \
    "tincidunt at. Cras a ipsum ex. Duis malesuada vulputate libero, et eleifend libero."


picture.draw(f, 300)

text = picture.decode("1.png")

print(text)
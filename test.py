import picture

f = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus quis orci diam. Ut porta dolor risus, fermentum sodales nisi semper sed."
picture.draw(f, 300, "111.png")

text = picture.decode("2.png")

print(text)

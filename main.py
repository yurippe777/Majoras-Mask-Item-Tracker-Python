import os
from PIL import Image, ImageTk
import tkinter as tk
import winsound
from idlelib.tooltip import Hovertip
from tkinter import messagebox
import sys

def reset_function():
    # ... code to save the game ...

    # Prompt user to confirm save
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to reset the game?")
    if not confirmed:
        return
    else:
        with open("misc_statuses.txt", "w") as f:
            # Write 28 lines with the number 0
            for i in range(19):
                f.write("0\n")
            f.write("1\n")
            for i in range (21,29):
                f.write("0\n")
            f.write("1\n")
        with open("mask_statuses.txt", "w") as f:
            # Write 24 lines with the number 0
            for i in range(24):
                f.write("0\n")
        with open("item_statuses.txt", "w") as f:
            # Write 24 lines with the number 0
            for i in range(24):
                f.write("0\n")


        python = sys.executable
        os.execl(python, python, *sys.argv)
        return

# User clicked "yes", so save the game
# ... code to save the game ...
# Load the 32x32 mask images
mask_images = []
item_images = []
misc_images = []
mask_names = []
item_names = []
misc_names = []
for i in range(24):
    filename = os.path.join("ICONS", f"mask_{i+1}.png")
    mask_image = Image.open(filename).convert("RGBA")
    mask_images.append(mask_image)
    mask_names.append(filename)

# Load the black and white versions of the mask images
bw_mask_images = []
bw_item_images = []
bw_misc_images = []
for i in range(24):
    filename = os.path.join("ICONS", f"mask_{i+1}bw.png")
    bw_mask_image = Image.open(filename).convert("RGBA")
    bw_mask_images.append(bw_mask_image)
for i in range(24):
    filename = os.path.join("ICONS2", f"item_{i+1}.png")
    item_image = Image.open(filename).convert("RGBA")
    item_images.append(item_image)
    item_names.append(filename)
for i in range (24):
    filename = os.path.join("ICONS2", f"item_{i+1}bw.png")
    bw_item_image = Image.open(filename).convert("RGBA")
    bw_item_images.append(bw_item_image)
for i in range (29):
    filename = os.path.join("ICONS3", f"misc_{i+1}.png")
    misc_image = Image.open(filename).convert("RGBA")
    misc_images.append(misc_image)
    misc_names.append(filename)
for i in range(27):
    if i == 19:
        i = i + 1
    filename = os.path.join("ICONS3",f"misc_{i+1}bw.png")
    bw_misc_image = Image.open(filename).convert("RGBA")
    bw_misc_images.append(bw_misc_image)
# Load the background image
bg_image = Image.open("pause_screen.png")
# Load the second background image
bg_image2 = Image.open("pause_screen2.png")
bg_image3 = Image.open("pause_screen3.png")
bg_image4 = Image.open("pause_screen4.png")
# Create a new image for the pause screen element
pause_screen_width = 240
pause_screen_height = 160
pause_screen = Image.new("RGBA", (pause_screen_width, pause_screen_height), (0, 0, 0, 0))
# Create a new image that is twice the height of the original pause screen image
combined_height = pause_screen_height * 2 + 21
combined_width = pause_screen_width * 2
combined_image = Image.new("RGBA", (combined_width, combined_height), (0, 0, 0, 0))

# Paste the first background image at the top of the combined image
combined_image.paste(bg_image, (0, 0))

# Paste the second background image below the first image
combined_image.paste(bg_image2, (0, pause_screen_height + 10))
combined_image.paste(bg_image3, (240, 0))
combined_image.paste(bg_image4, (240,170))
# Create a window and display the combined image
root = tk.Tk()
root.title("Majora's Mask")

# Set the minimum size of the window to the size of the combined image
root.minsize(combined_image.width, combined_image.height)

# Create a frame for the pause screen and pack it in the window
pause_screen_frame = tk.Frame(root)
pause_screen_frame.pack(fill=tk.BOTH, expand=True)

# Convert the image to a PhotoImage object and display it in a label
img = ImageTk.PhotoImage(combined_image)
label = tk.Label(pause_screen_frame, image=img)
label.pack(fill=tk.BOTH, expand=True)

# Set the position of the pause screen element as a proportion of the window size
pause_screen_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Paste the mask images onto the pause screen element as buttons
mask_width = 32
mask_height = 32
x_offset = (pause_screen_width - (6 * mask_width)) // 2
y_offset = ((pause_screen_height - (4 * mask_height)) // 2) + 10  # shift down by 10 pixels

mask_buttons = []
item_buttons = []
misc_buttons = []
with open("misc_statuses.txt", "r") as f:
    misc_statuses = f.read().splitlines()
# Create a function to toggle between the colored and black-and-white versions of the masks
# Create a function to toggle between the colored and black-and-white versions of the masks
def toggle_mask(button):
    # Get the index of the button that was clicked
    button_index = mask_buttons.index(button)

    # Get the current image on the button
    current_image = button.image
    current_name = mask_names[button_index]

    # Determine the new image to display
    if "bw" in current_name:
        new_name = current_name.replace("bw.png", ".png")
        status = "1"
        sound_file = "SOUNDS/Select.wav"
    else:
        new_name = current_name.replace(".png", "bw.png")
        status = "0"
        sound_file = "SOUNDS/Deselect.wav"

    # Load the new image and update the button image
    new_image = ImageTk.PhotoImage(Image.open(new_name))
    button.configure(image=new_image)
    button.image = new_image

    # Update the mask_names and mask_statuses lists with the new filename and status
    mask_names[button_index] = new_name
    mask_statuses[button_index] = status

    # Save the status of each button to a text file
    with open("mask_statuses.txt", "w") as f:
        for status in mask_statuses:
            f.write(status + "\n")

    # Play the appropriate sound
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)
def toggle_item(button):
    # Get the index of the button that was clicked
    button_index = item_buttons.index(button)

    # Get the current image on the button
    current_image = button.image
    current_name = item_names[button_index]

    # Determine the new image to display
    if current_name != "item_2.png" or "item_2x.png" or "item_2y.png" or "item_2bw.png" or "item_7.png" or "item_7x.png" or "item_7y.png" or "item_7bw.png":
        if "bw" in current_name:
            new_name = current_name.replace("bw.png", ".png")
            status = "1"
            sound_file = "SOUNDS/Select.wav"
        else:
            new_name = current_name.replace(".png", "bw.png")
            status = "0"
            sound_file = "SOUNDS/Deselect.wav"
    if button_index == 1 or button_index == 6:
        if "bw" in current_name:
            new_name = current_name.replace("bw.png", ".png")
            status = "1"
            sound_file = "SOUNDS/Select.wav"
        elif "x" in current_name:
            new_name = current_name.replace("x.png", "y.png")
            status = "3"
            sound_file = "SOUNDS/Select.wav"
        elif "y" in current_name:
            new_name = current_name.replace("y.png", "bw.png")
            status = "0"
            sound_file = "SOUNDS/Select.wav"
        else:
            new_name = current_name.replace(".png", "x.png")
            status = "2"
            sound_file = "SOUNDS/Deselect.wav"

    # Load the new image and update the button image
    new_image = ImageTk.PhotoImage(Image.open(new_name))
    button.configure(image=new_image)
    button.image = new_image

    # Update the mask_names and mask_statuses lists with the new filename and status
    item_names[button_index] = new_name
    item_statuses[button_index] = status
    # Save the status of each button to a text file
    with open("item_statuses.txt", "w") as f:
        for status in item_statuses:
            f.write(status + "\n")

    # Play the appropriate sound
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)
def toggle_misc(button):
    # Get the index of the button that was clicked
    button_index = misc_buttons.index(button)

    # Get the current image on the button
    current_image = button.image
    current_name = misc_names[button_index]

    # Determine the new image to display
    if "bw" in current_name:
        new_name = current_name.replace("bw.png", ".png")
        status = "1"
        sound_file = "SOUNDS/Select.wav"
    #elif button_index == 19:
      #  new_name = current_name
      #  status = "1"
      #  sound_file = "SOUNDS/Select.wav"
    elif (button_index in [15,16,17,19,25,27]) and "bw" not in current_name and "x" not in current_name and "y" not in current_name and "z" not in current_name:
        new_name = current_name.replace(".png","x.png")
        status = "2"
        sound_file = "SOUNDS/Select.wav"
    elif (button_index in [15,19,25,27]) and "x" in current_name:
        new_name = current_name.replace("x.png","y.png")
        status = "3"
        sound_file = "SOUNDS/Select.wav"
    elif (button_index in [19,27] and "y" in current_name):
        new_name = current_name.replace("y.png","z.png")
        status = "4"
        sound_file = "SOUNDS/Select.wav"
    elif (button_index ==19 and "z" in current_name):
        new_name = current_name.replace("z.png",".png")
        status = "1"
        sound_file = "SOUNDS/Select.wav"
    elif (button_index ==27 and "z" in current_name):
        new_name = current_name.replace("z.png","bw.png")
        status = "0"
        sound_file = "SOUNDS/Select.wav"
    elif (button_index ==16 or button_index ==17) and "x" in current_name:
        new_name = current_name.replace("x.png","bw.png")
        status = "0"
        sound_file = "SOUNDS/Select.wav"
    elif (button_index in [15,25]) and "y" in current_name:
        new_name = current_name.replace("y.png","bw.png")
        status = "0"
        sound_file = "SOUNDS/Select.wav"
    else:
        new_name = current_name.replace(".png", "bw.png")
        status = "0"
        sound_file = "SOUNDS/Deselect.wav"

    # Load the new image and update the button image
    if button_index != 28:
        new_image = ImageTk.PhotoImage(Image.open(new_name))
        button.configure(image=new_image)
        button.image = new_image
    else:
        new_name = current_name
        status = "1"
        reset_function()

    # Update the misc_names and misc_statuses lists with the new filename and status
    misc_names[button_index] = new_name
    misc_statuses[button_index] = status

    # Save the status of each button to a text file
    with open("misc_statuses.txt", "w") as f:
        for status in misc_statuses:
            f.write(status + "\n")

    # Play the appropriate sound
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)
# Add the mask buttons to the pause screen element
mask_buttons = []
item_buttons = []
misc_buttons = []
with open("mask_statuses.txt", "r") as f:
    mask_statuses = f.read().splitlines()

for i, mask_image in enumerate(mask_images):
    # Create the button and add it to the list of buttons
    if mask_statuses[i] == "0":
        button_image = ImageTk.PhotoImage(bw_mask_images[i])
    else:
        button_image = ImageTk.PhotoImage(mask_image)
    button = tk.Button(pause_screen_frame, image=button_image, bg='#555555', text = "?")
    button.pack(pady=30)
    mask_dict = {
        0: "Postman's Hat",
        1: "All-Night Mask",
        2: "Blast Mask",
        3: "Stone Mask",
        4: "Great Fairy's Mask",
        5: "Deku Mask",
        6: "Keaton Mask",
        7: "Bremen Mask",
        8: "Bunny Hood",
        9: "Don Gero's Mask",
        10: "Mask of Scents",
        11: "Goron Mask",
        12: "Romani's Mask",
        13: "Circus Leader's Mask",
        14: "Kafei's Mask",
        15: "Couple's Mask",
        16: "Mask of Truth",
        17: "Zora Mask",
        18: "Kamaro's Mask",
        19: "Gibdo Mask",
        20: "Garo's Mask",
        21: "Captain's Hat",
        22: "Giant's Mask",
        23: "Fierce Deity's Mask",
    }

    myTip = Hovertip(button, mask_dict.get(i, ":3"))

    button.image = button_image
    mask_buttons.append(button)

    # Set the position of the button as a proportion of the window size
    x = x_offset + ((i % 6) * mask_width)
    y = y_offset + ((i // 6) * mask_height)
    button.place(x=x, y=y)

    # Bind the toggle_mask function to the button
    button.configure(command=lambda b=button: toggle_mask(b))

    # Simulate a click on the button to toggle the image if it's black and white
    if mask_statuses[i] == "0":
        button.invoke()



#########################################################################################################################
with open("item_statuses.txt", "r") as f:
    item_statuses = f.read().splitlines()

for i, item_image in enumerate(item_images):
    # Create the button and add it to the list of buttons
    if item_statuses[i] == "0":
        button_image = ImageTk.PhotoImage(bw_item_images[i])
    else:
        button_image = ImageTk.PhotoImage(item_image)
    button = tk.Button(pause_screen_frame, image=button_image, bg='#555555', text = "?")
    button.pack(pady=30)
    button.image = button_image
    item_buttons.append(button)

    # Set the position of the button as a proportion of the window size
    x = x_offset + ((i % 6) * mask_width)
    y = y_offset + ((i // 6) * mask_height) + 170
    button.place(x=x, y=y)

    # Bind the toggle_item function to the button
    button.configure(command=lambda b=button: toggle_item(b))

    # Simulate a click on the button to toggle the image if it's black and white
    if i != 6 and i !=1:
        if item_statuses[i] == "0":
            button.invoke()
    if i == 1 or i == 6:
        if item_statuses[i] == "0":
            for _ in range(3):
                button.invoke()
        if item_statuses[i] == "1":
            for _ in range(4):
                button.invoke()
        if item_statuses[i] == "2":
            for _ in range(1):
                button.invoke()
        if item_statuses[i] == "3":
            for _ in range(2):
                button.invoke()
    mask_dict = {
        0: "Ocarina of Time",
        1: "Hero's Bow" ,
        2: "Fire Arrow",
        3: "Ice Arrow",
        4: "Light Arrow",
        5: "Moon's Tear",
        6: "Bomb Bag",
        7: "Bombchu",
        8: "Deku Stick",
        9: "Deku Nut",
        10: "Magic Bean",
        11: "Room Key",
        12: "Powder Keg",
        13: "Pictograph Box",
        14: "Lens of Truth",
        15: "Hookshot",
        16: "Great Fairy's Sword",
        17: "Letter to Kafei",
        18: "Bottle #1",
        19: "Bottle #2",
        20: "Bottle #3",
        21: "Bottle #4",
        22: "Bottle #5",
        23: "Bottle #6",
    }

    myTip = Hovertip(button, mask_dict.get(i, ":3"))
#########################################################################################################################
with open("misc_statuses.txt", "r") as f:
    misc_statuses = f.read().splitlines()
for i, misc_image in enumerate(misc_images):
    # Create the button and add it to the list of buttons
   # if misc_statuses[i] == "0":
    #    button_image = ImageTk.PhotoImage(bw_misc_images[i])
    #else:
    button_image = ImageTk.PhotoImage(misc_image)
    button = tk.Button(pause_screen_frame, image=button_image, bg='#555555', text = "?")
    button.pack(pady=30)
    mask_dict = {
        0: "Bombers' Notebook",
        1: "Odolwa's Remains" ,
        2: "Gyorg's Remains",
        3: "Goht's Remains",
        4: "Twinmold's Remains",
        5: "Song of Time",
        6: "Song of Healing",
        7: "Epona's Song",
        8: "Song of Soaring",
        9: "Song of Storms",
        10: "Sonata of Awakening",
        11: "Goron Lullaby",
        12: "New Wave Bossa Nova",
        13: "Elegy of Emptiness",
        14: "Oath to Order",
        15: "Kokiri/Razor/Guilded Sword",
        16: "Hylian/Mirror Shield",
        17: "Magic",
        18: "Double Defense",
        19: "Wallet",
        20: "Woodfall Temple Boss Key",
        21: "Snowhead Temple Boss Key",
        22: "Great Bay Temple Boss Key ",
        23: "Stone Tower Temple Boss Key",
        24: "Woodfall Temple Small Key",
        25: "Snowhead Temple Small Keys",
        26: "Great Bay Temple Small Key",
        27: "Stone Tower Temple Small Keys",
        28: "RESET",
    }

    myTip = Hovertip(button, mask_dict.get(i, ":3"))
    button.image = button_image
    misc_buttons.append(button)

    # Set the position of the button as a proportion of the window size
    if i != 0:
        x = x_offset + ((i % 6) * mask_width) + 500
        y = y_offset + ((i // 6) * mask_height)
        button.place(x=x, y=y)
    if i == 0:
        x = x_offset + ((i % 6) * mask_width) + 220
        y = y_offset + ((i // 6) * mask_height) -20
        button.place(x=x, y=y)
    if i == 1:
        x = x_offset + ((i % 6) * mask_width) + 346
        y = y_offset + ((i // 6) * mask_height) - 4
        button.place(x=x, y=y)

    if i == 2:
        x = x_offset + ((i % 6) * mask_width) + 277
        y = y_offset + ((i // 6) * mask_height) + 15
        button.place(x=x, y=y)
    if i == 3:
        x = x_offset + ((i % 6) * mask_width) + 320
        y = y_offset + ((i // 6) * mask_height) + 15
        button.place(x=x, y=y)
    if i == 4:
        x = x_offset + ((i % 6) * mask_width) + 250
        y = y_offset + ((i // 6) * mask_height) + 35
        button.place(x=x, y=y)
    if i == 5:
        x = 280
        y = 6
        button.place(x=x, y=y)
    if i == 6:
        x = 243
        y = 44
        button.place(x=x, y=y)
    if i == 7:
        x = 280
        y = 44
        button.place(x=x, y=y)
    if i == 8:
        x = 317
        y = 44
        button.place(x=x, y=y)
    if i == 9:
        x = 243
        y = 81
        button.place(x=x, y=y)
    if i == 10:
        x = 280
        y = 81
        button.place(x=x, y=y)
    if i == 11:
        x = 317
        y = 81
        button.place(x=x, y=y)
    if i == 12:
        x = 243
        y = 118
        button.place(x=x, y=y)
    if i == 13:
        x = 280
        y = 118
        button.place(x=x, y=y)
    if i == 14:
        x = 317
        y = 118
        button.place(x=x, y=y)
    if i == 15:
        x = 364
        y = 90
        button.place(x=x, y=y)
    if i == 16:
        x = 440
        y = 90
        button.place(x=x, y=y)
    if i == 17:
        x = 364
        y = 128
        button.place(x=x, y=y)
    if i == 18:
        x = 317
        y = 6
        button.place(x=x, y=y)
    if i == 19:
        x = 440
        y = 128
        button.place(x=x, y=y)
    if i == 20:
        x = 320
        y = 200
        button.place(x=x, y=y)
    if i == 21:
        x = 357
        y = 200
        button.place(x=x, y=y)
    if i == 22:
        x = 394
        y = 200
        button.place(x=x, y=y)
    if i == 23:
        x = 431
        y = 200
        button.place(x=x, y=y)
    if i == 24:
        x = 320
        y = 237
        button.place(x=x, y=y)
    if i == 25:
        x = 357
        y = 237
        button.place(x=x, y=y)
    if i == 26:
        x = 394
        y = 237
        button.place(x=x, y=y)
    if i == 27:
        x = 431
        y = 237
        button.place(x=x, y=y)
    if i == 28:
        x = 257
        y = 282
        button.place(x=x, y=y)
    # Bind the toggle_misc function to the button
    button.configure(command=lambda b=button: toggle_misc(b))

    # Simulate a click on the button to toggle the image if it's black and white
    if i != 15 and i !=16 and i!= 17 and i!= 19 and i!=25:
        if misc_statuses[i] == "0":
            button.invoke()
    if i == 15 or i ==16 or i ==17 or i ==19 or i==25 or i==27:
        if misc_statuses[i] == "0" and i !=16 and i !=17:
            for _ in range(3):
                button.invoke()
        if misc_statuses[i] == "0" and (i ==16 or i==17):
            for _ in range(1):
                button.invoke()
        if i == 27 and misc_statuses[i] == "0":
            for _ in range(4):
                button.invoke()
        if misc_statuses[i] == "1" and (i != 16 and i!=17 and i!=27):
            for _ in range(4):
                button.invoke()
        if misc_statuses[i] == "2":
            for _ in range(1):
                button.invoke()
        if misc_statuses[i] == "3":
            for _ in range(2):
                button.invoke()
        if misc_statuses[i] == "4":
            for _ in range(3):
                button.invoke()
# Start the main event loop
winsound.PlaySound("SOUNDS/Startup.wav", winsound.SND_ASYNC)
root.mainloop()
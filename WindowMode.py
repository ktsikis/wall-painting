from tkinter import *
from tkinter import filedialog, messagebox
import wall_paint as wp
import cv2
from PIL import ImageColor

my_color = '#990099'

picture = None
blend = None

# creating root window
root = Tk()
root.title('Coloring Your Wall')
root.geometry('500x500')

# canvas to check witch color to apply in image selected area
color_canvas = Canvas(root, width='200', height='200', bg='#990099')
color_canvas.grid(row=0, column=1)

# sample colors for wall
colors_frame = LabelFrame(root, text='Colors for your wall')
colors_frame.grid(row=0, column=0)

# color bars to create any color on RGB formation
color_bars_frame = LabelFrame(root, text='Create your own color')
color_bars_frame.grid(row=1)


def select_texture():
    global picture, blend, texture_image
    if picture is None:
        messagebox.showwarning('Warning!', 'Please select image first')
    else:
        texture_file = filedialog.askopenfilename(
            title='Select a texture', filetypes=(('jpeg files', '*.jpg'), ('png files', '*.png'), ('all files', '*.*'))
        )
        texture_image = cv2.imread(texture_file)
        blend = wp.Blending_Mode('Blend', image, picture.get_mask(), texture_image, blend_type='Texture')


def texture_set(mode):
    global picture, blend, texture_image
    color = ImageColor.getcolor(str(my_color), 'RGB')
    color = color[::-1]
    blend.set_blend(texture_image)
    blend.update_mask(picture.get_mask())
    picture.refresh()
    if mode == 'with out':
        blend.start_blending()
    elif mode == 'with':
        blend.paint_texture_with(color)
        blend.start_blending()
    blend.show_out_image()


# area for texture in selected wall
texture_frame = LabelFrame(root, text='Select Texture for your wall')
texture_frame.grid(row=2)
texture_button = Button(texture_frame, text='Select texture', command=select_texture)
texture_button.grid(row=0)
texture_color = Button(texture_frame, text='Blend with color', command=lambda: texture_set('with'))
texture_color.grid(row=1)
texture_without_color = Button(texture_frame, text='Blend without color', command=lambda: texture_set('with out'))
texture_without_color.grid(row=2)


def image_normalize(img):
    h, w = img.shape[:2]
    print(h,w)
    scale = 100
    if h > 1500 or w > 2000:
        print('Image has been resized')
        if w > h:
            print('here')
            scale = w / 200
        else:
            print('there')
            scale = h / 150
        width = int(w * scale / 100)
        height = int(h * scale / 100)
        dim = (width, height)
        print(dim)
        newimg = cv2.resize(img, dim)
    else:
        newimg = img.copy()
    return newimg


# func to open image (File -> Open)
def open_image():
    global picture, blend, image
    image_file = filedialog.askopenfilename(
        title='Select an image to edit',
        filetypes=(('jpeg files', '*.jpg'), ('png files', '*.png'), ('all files', '*.*'))
    )
    image = cv2.imread(image_file)
    image = image_normalize(image)
    print(image.shape)
    picture = wp.Selection_Mode('Picture', image)
    blend = wp.Blending_Mode('Blend', image, picture.get_mask())
    picture.show_image()


# func to save image after editing (File -> Save)
def save_image():
    global picture, blend
    if blend is None:
        messagebox.showwarning('Warning!', 'Please select image first')
    else:
        image_file = filedialog.asksaveasfile(
            mode='w', title='Save Figure',
            defaultextension='.jpg',
            filetypes=(('jpg files', '*.jpg'), ('png files', '*.png'), ('all files', '*.*'))
        )
        if image_file is None:
            return None
        print(image_file.name)
        cv2.imwrite(str(image_file.name), blend.get_out_image())


# func to set color from samples
def set_default_color(color):
    global my_color
    color_canvas.config(bg=str(color))
    my_label = Label(root, text='You choose this color in hex: ' + str(my_color)).grid(row=1, column=1)
    my_color = color


# func to set color from RGB bars
def get_color(var):
    global my_color
    hex_color = '#%02x%02x%02x' % (int(red.get()), int(green.get()), int(blue.get()))
    color_canvas.config(bg=str(hex_color))
    my_label = Label(root, text='You choose this color in hex: ' + str(my_color)).grid(row=1, column=1)
    my_color = hex_color


# func to apply color on wall at image
def set_color():
    global picture, blend
    color = ImageColor.getcolor(str(my_color), 'RGB')
    color = color[::-1]
    my_label = Label(root, text='You choose this color in hex: ' + str(my_color)).grid(row=1, column=1)
    if picture is None:
        messagebox.showwarning('Warning!', 'Please select image first')
    else:
        blend.set_blend(color)
        blend.update_mask(picture.get_mask())
        picture.refresh()
        blend.start_blending()
        blend.show_out_image()


# color bars and labels to create RGB colors

# red bar
red_label = Label(color_bars_frame, text='Red:').grid(row=0, column=0)
red = Scale(color_bars_frame, from_=0, to=255, orient=HORIZONTAL, command=get_color)
red.grid(row=0, column=1)

# green bar
green_label = Label(color_bars_frame, text='Green:').grid(row=1, column=0)
green = Scale(color_bars_frame, from_=0, to=255, orient=HORIZONTAL, command=get_color)
green.grid(row=1, column=1)

# blue bar
blue_label = Label(color_bars_frame, text='Blue:').grid(row=2, column=0)
blue = Scale(color_bars_frame, from_=0, to=255, orient=HORIZONTAL, command=get_color)
blue.grid(row=2, column=1)

blend_button = Button(color_bars_frame, text='Start Blending', command=set_color)
blend_button.grid(row=3, column=0, columnspan=2)

# create buttons
# reds
button_1 = Button(colors_frame, height=2, width=2, bg='#F28500', command=lambda: set_default_color('#F28500')).grid(
    row=0, column=0)  # Tangerine
button_2 = Button(colors_frame, height=2, width=2, bg='#E30B5C', command=lambda: set_default_color('#E30B5C')).grid(
    row=0, column=1)  # Raspberry
button_3 = Button(colors_frame, height=2, width=2, bg='#DC143C', command=lambda: set_default_color('#DC143C')).grid(
    row=0, column=2)  # Crimson

# greens
button_4 = Button(colors_frame, height=2, width=2, bg='#3EB489', command=lambda: set_default_color('#3EB489')).grid(
    row=1, column=0)  # Mind Green
button_5 = Button(colors_frame, height=2, width=2, bg='#5E716A', command=lambda: set_default_color('#5E716A')).grid(
    row=1, column=1)  # Grey-Green
button_6 = Button(colors_frame, height=2, width=2, bg='#4B5320', command=lambda: set_default_color('#4B5320')).grid(
    row=1, column=2)  # Army Green

# blues
button_7 = Button(colors_frame, height=2, width=2, bg='#89CFF0', command=lambda: set_default_color('#89CFF0')).grid(
    row=2, column=0)  # Baby Blue
button_8 = Button(colors_frame, height=2, width=2, bg='#0077BE', command=lambda: set_default_color('#0077BE')).grid(
    row=2, column=1)  # Ocean Blue
button_9 = Button(colors_frame, height=2, width=2, bg='#4682B4', command=lambda: set_default_color('#4682B4')).grid(
    row=2, column=2)  # Steel Blue

# whites
button_10 = Button(colors_frame, height=2, width=2, bg='#FFFDD0', command=lambda: set_default_color('#FFFDD0')).grid(
    row=3, column=0)  # Cream
button_11 = Button(colors_frame, height=2, width=2, bg='#C8A2C8', command=lambda: set_default_color('#C8A2C8')).grid(
    row=3, column=1)  # Lilac
button_12 = Button(colors_frame, height=2, width=2, bg='#F5F5DC', command=lambda: set_default_color('#F5F5DC')).grid(
    row=3, column=2)  # Beige

# blacks
button_13 = Button(colors_frame, height=2, width=2, bg='#241914', command=lambda: set_default_color('#241914')).grid(
    row=4, column=0)  # Bark Brown
button_14 = Button(colors_frame, height=2, width=2, bg='#555D50', command=lambda: set_default_color('#555D50')).grid(
    row=4, column=1)  # Ebony
button_15 = Button(colors_frame, height=2, width=2, bg='#2A3439', command=lambda: set_default_color('#2A3439')).grid(
    row=4, column=2)  # Gunmetal

# first menu
menuBar = Menu(root)
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label='Open', command=open_image)
fileMenu.add_command(label='Save', command=save_image)
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=root.destroy)
menuBar.add_cascade(label='File', menu=fileMenu)

# mode menu
modeMenu = Menu(menuBar, tearoff=0)
modeMenu.add_command(label='Magic Tool', command=lambda: picture.set_select_mode('MagicTool'))
modeMenu.add_command(label='Polygon', command=lambda: picture.set_select_mode('Polygon'))
menuBar.add_cascade(label='Selection Mode', menu=modeMenu)

# blend menu
blendMenu = Menu(menuBar, tearoff=0)
blendMenu.add_command(label='Normal', command=lambda: blend.set_blend_mode('Normal'))
blendMenu.add_separator()
blendMenu.add_command(label='Addition', command=lambda: blend.set_blend_mode('Addition'))
blendMenu.add_command(label='Divide', command=lambda: blend.set_blend_mode('Divide'))
blendMenu.add_command(label='Subtract', command=lambda: blend.set_blend_mode('Subtract'))
blendMenu.add_separator()
blendMenu.add_command(label='Multiply', command=lambda: blend.set_blend_mode('Multiply'))
blendMenu.add_command(label='Darken', command=lambda: blend.set_blend_mode('Darken'))
blendMenu.add_separator()
blendMenu.add_command(label='Screen', command=lambda: blend.set_blend_mode('Screen'))
blendMenu.add_command(label='Lighten', command=lambda: blend.set_blend_mode('Lighten'))
blendMenu.add_separator()
blendMenu.add_command(label='Overlay', command=lambda: blend.set_blend_mode('Overlay'))
blendMenu.add_command(label='Soft Light', command=lambda: blend.set_blend_mode('Soft Light'))
blendMenu.add_command(label='Hard Light', command=lambda: blend.set_blend_mode('Hard Light'))
menuBar.add_cascade(label='Blend Mode', menu=blendMenu)

#help menu
helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label='Instructions')
helpMenu.add_separator()
helpMenu.add_command(label='Application Info')
menuBar.add_cascade(label='Help', menu=helpMenu)
# display menu
root.config(menu=menuBar)
messagebox.showinfo('This is an advice!', 'Please check the help section in the menu bar for instructions!')

root.mainloop()

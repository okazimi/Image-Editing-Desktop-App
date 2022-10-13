from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageGrab
import os

# GLOBAL VARIABLES
# INITIALIZE WINDOW
home_window = Tk()
# INITIALIZE IMAGE FILE PATH STORAGE VARIABLE
all_files = list()
# INITIALIZE IMAGE BUTTON COUNT VARIABLE
add_images_button_count = 0
# INITIALIZE X AND Y POSITION FOR IMAGE PLACEMENT ON HOME SCREEN
x = 0
y = 0
# INITIALIZE MAX IMAGE COUNT VARIABLE FOR HOME SCREEN
max_image = []
# INITIALIZE CANVAS
canvas = Canvas(home_window, width=600, height=400, bg="white")
# INITIALIZE CURRENT IMAGE
current_image = None
# INITIALIZE IMAGE COUNTER
image_counter = 0
# INITIALIZE IMAGE CONTAINER FOR CANVAS
image_container = None


# HOME SCREEN
def home_screen():
    # REFERENCE GLOBAL WINDOW
    global home_window, canvas

    # CREATE CANVAS
    canvas.place(rely=0.1)

    # SPECIFY WINDOW SIZE
    home_window.geometry("600x450")

    # SPECIFY WINDOW TITLE
    home_window.title("Foto Editor")

    # CREATES TOP FRAME
    header_frame = Frame(home_window, width=600, height=50, bd=5, bg="grey")
    header_frame.grid(row=0)

    # BUTTONS
    close = Button(header_frame, text="Close App", bg="white", fg="blue", command=close_app)
    close.place(relx=0.015, rely=0.2, anchor="nw")

    back = Button(header_frame, text="Back", bg="white", fg="blue", state="disabled")
    back.place(relx=0.13, rely=0.2, anchor="nw")

    add_images = Button(header_frame, text="Add Images", bg="white", fg="blue", command=add_button)
    add_images.place(relx=0.45, rely=0.2, anchor="n")

    clear = Button(header_frame, text="Clear", bg="white", fg="blue", command=clear_image_uploads)
    clear.place(relx=0.55, rely=0.2, anchor="n")

    next_step = Button(header_frame, text="Next Step", bg="blue", fg="white", command=next_step_button)
    next_step.place(relx=0.985, rely=0.2, anchor="ne")

    # RUN A NON RESIZEABLE TKINTER WINDOW
    home_window.resizable(False, False)
    # CLOSING WINDOW PROTOCOL
    home_window.protocol("WM_DELETE_WINDOW", close_app)
    # RUN WINDOW
    home_window.mainloop()


# EDITING SCREEN
def edit_screen():
    # REFERENCE GLOBAL VARIABLES
    global home_window, current_image, image_counter, all_files, image_container, canvas, add_images_button_count, \
        max_image

    # CLEAR PREVIOUS WINDOW CANVAS
    clear_screen()

    # SPECIFY WINDOW SIZE
    home_window.geometry("600x450")

    # CREATES TOP FRAME
    header_frame = Frame(home_window, width=600, height=50, bd=5, bg="grey")
    header_frame.grid(row=0)

    # BUTTONS
    close = Button(header_frame, text="Close App", bg="white", fg="blue", command=close_app)
    close.place(relx=0.015, rely=0.2, anchor="nw")

    back = Button(header_frame, text="Back", bg="white", fg="blue", command=back_button)
    back.place(relx=0.13, rely=0.2, anchor="nw")

    add_text = Button(header_frame, text="Add Text", bg="white", fg="blue", command=add_text_button)
    add_text.place(relx=0.38, rely=0.2, anchor="nw")

    add_logo = Button(header_frame, text="Add Logo", bg="white", fg="blue", command=add_logo_button)
    add_logo.place(relx=0.485, rely=0.2, anchor="nw")

    clear = Button(header_frame, text="Clear", bg="white", fg="blue", command=clear_edits)
    clear.place(relx=0.63, rely=0.2, anchor="n")

    save = Button(header_frame, text="Save", bg="blue", fg="white", command=save_button)
    save.place(relx=0.985, rely=0.2, anchor="ne")

    # MULTIPLE IMAGE ERROR HANDLING
    # TRY TO LOOP THROUGH FILES AND DISPLAY IMAGE
    try:
        # LOGIC TO DISPLAY EACH PICTURE
        # OBTAIN DESIRED IMAGE FILE
        f = all_files[image_counter]
        # OPEN FILE AS IMAGE
        current_image = Image.open(f)
        # CONVERT TO TK PHOTO IMAGE
        resized_img = ImageTk.PhotoImage(current_image.resize((500, 400)))
        # CREATE IMAGE ON CANVAS
        image_container = canvas.create_image(300, 210, image=resized_img)
    # CATCH INDEX ERROW WHEN ACCESSING FILES
    except IndexError:
        # RESET IMAGE BUTTON COUNT VARIABLE
        add_images_button_count = 0
        # RESET MAX IMAGE COUNT VARIABLE
        max_image = []
        # RESET IMAGE COUNTER
        image_counter = 0
        # REDIRECT TO HOME SCREEN
        home_screen()

    # RUN A NON RESIZEABLE TKINTER WINDOW
    home_window.resizable(False, False)
    # CLOSING WINDOW PROTOCOL
    home_window.protocol("WM_DELETE_WINDOW", close_app)
    # RUN WINDOW
    home_window.mainloop()


# BACK BUTTON
def back_button():
    # REFERENCE GLOBAL VARIABLES
    global canvas, image_container, all_files, add_images_button_count, max_image, image_counter
    # CLEAR IMAGES FROM CANVAS
    canvas.delete("all")
    # RESET IMAGE COUNTER
    image_counter = 0
    # RESET UPLOADED IMAGES COUNT
    add_images_button_count = 0
    # RESET ALL FILES
    all_files = list()
    max_image = []
    # REDIRECT TO HOME SCREEN
    home_screen()


# ADD IMAGES BUTTON
def add_button():
    # REFERENCE GLOBAL VARIABLES
    global home_window, canvas, add_images_button_count, x, y, max_image, all_files
    # SPECIFY FILE TYPES
    filetypes = [('JPG Files', '*.jpg'), ('PNG Files', '*.png')]
    # OPEN FILE EXPLORER AND ALLOW USER TO SELECT PHOTO
    filename = askopenfilename(multiple=True, filetypes=filetypes)
    # STORE ALL FILES
    all_files.extend(filename)
    # APPEND NEW FILE TO MAX IMAGE COUNTER
    max_image.append(filename)
    # CHECK IF MAX IMAGE AMOUNT OF 6 IS REACHED, INFORM USER
    if len(max_image) > 6:
        max_image_warning()
        return
    # FIRST CLICK
    if add_images_button_count == 0:
        # START POSITION FOR IMAGE
        x = 0.1
        y = 0.25
        # INCREMENT BUTTON COUNTER
        add_images_button_count += 1
    # NOT FIRST CLICK
    else:
        # IMAGE POSITIONING LOGIC
        # START NEW ROW AFTER THIRD COLUMN
        if x == 0.7:
            x = 0.1
            y = 0.6
            # INCREMENT BUTTON COUNTER
            add_images_button_count += 1
        # ELSE CONTINUE TO INCREMENT COLUMN
        else:
            x += 0.3
            # INCREMENT BUTTON COUNTER
            add_images_button_count += 1
    # MULTIPLE IMAGES METHOD
    for f in filename:
        # OPEN AS IMAGE
        img = Image.open(f)
        # RESIZE IMAGE
        img_resized = img.resize((100, 100))
        # CONVERT IMAGE TO TK PHOTO IMAGE
        img = ImageTk.PhotoImage(img_resized)
        # CREATE LABEL TO DISPLAY IMAGE
        panel = Label(canvas)
        # IMAGE POSITION
        panel.place(relx=x, rely=y)
        # ASSIGN IMAGE TO LABEL DIRECTLY
        panel.image = img
        # GARBAGE COLLECTION
        panel['image'] = img


# CLEAR IMAGE UPLOADS
def clear_image_uploads():
    # REFERENCE GLOBAL VARIABLE
    global canvas, add_images_button_count, all_files, max_image
    # RESET ALL FILES
    all_files = []
    max_image = []
    # CLEAR IMAGES
    for child in canvas.winfo_children():
        child.destroy()
    # RESET BUTTON COUNTER TO ZERO
    add_images_button_count = 0


# CLEAR IMAGE EDITS
def clear_edits():
    # TRY TO REMOVE PREVIOUSLY EDITED IMAGE
    try:
        # DELETE PREVIOUSLY EDITED IMAGE
        os.remove("assets/Edit.jpg")
    # CATCH INSTANCE WHERE EDIT IMAGE FILE DOES NOT EXIST
    except FileNotFoundError:
        pass
    # REROUTE BACK TO HOME SCREEN
    finally:
        # REDIRECT BACK TO EDIT SCREEN
        edit_screen()


# GENERIC CLEAR SCREEN FUNCTION
def clear_screen():
    # REFERENCE GLOBAL VARIABLES
    global canvas, add_images_button_count
    # CLEAR IMAGES ON CANVAS
    for child in canvas.winfo_children():
        child.destroy()
    # RESET BUTTON COUNTER TO ZERO
    add_images_button_count = 0


# NEXT STEP BUTTON
def next_step_button():
    # REFERENCE GLOBAL VARIABLES
    global home_window, all_files
    # TRY TO NAVIGATE TO EDIT SCREEN
    try:
        # REDIRECT TO EDIT SCREEN
        edit_screen()
    # CATCH EXCEPTION WHERE USER HASN'T SELECTED PHOTOS YET
    except TypeError:
        # PROMPT USER TO SELECT PHOTOS BEFORE CONTINUING
        # INITIALIZE POP-UP WINDOW
        pop = Toplevel(home_window)
        # SET POP-UP WINDOW SIZE
        pop.geometry("300x200")
        # SET TITLE FOR WINDOW
        pop.title("Warning")
        # SET WARNING MESSAGE
        Label(pop, text="Please select at least one photo to continue!").pack(pady=20)
        # CREATE BUTTON
        Button(pop, text="Understood", command=pop.destroy).pack(pady=40)
        # REROUTE BACK TO HOME SCREEN
        home_screen()
    # CATCH EXCEPTION WHERE USER HASN'T SELECTED PHOTOS YET
    except IndexError:
        # PROMPT USER TO SELECT PHOTOS BEFORE CONTINUING
        # INITIALIZE POP-UP WINDOW
        pop = Toplevel(home_window)
        # SET POP-UP WINDOW SIZE
        pop.geometry("300x200")
        # SET TITLE FOR WINDOW
        pop.title("Warning")
        # SET WARNING MESSAGE
        Label(pop, text="Please select at least one photo to continue!").pack(pady=20)
        # CREATE BUTTON
        Button(pop, text="Understood", command=pop.destroy).pack(pady=40)
        # REROUTE BACK TO HOME SCREEN
        home_screen()


# SAVE BUTTON
def save_button():
    # REFERENCE GLOBAL VARIABLES
    global current_image, image_counter, all_files, add_images_button_count, max_image, canvas, image_container
    # SPECIFY FILE TYPES
    filetypes = [('JPG Files', '*.jpg'), ('PNG Files', '*.png')]
    # PROMPT USER TO SAVE IMAGE
    file = asksaveasfilename(defaultextension=".jpg", filetypes=filetypes)
    # ERROR HANDLING FOR SAVING PICTURE
    try:
        # OPEN IMAGE
        current_image = ImageTk.getimage(current_image)
        # CONVERT IMAGE
        current_image = current_image.convert('RGB')
        # SAVE IMAGE
        current_image.save(file)
        # INCREASE IMAGE COUNTER
        image_counter += 1
    # CATCH TYPE ERROR (A.K.A NO EDIT TO PICTURE MADE)
    except TypeError:
        # SAVE IMAGE
        current_image.save(file)
        # INCREASE IMAGE COUNTER
        image_counter += 1
    # EXECUTE NO MATTER WHAT
    finally:
        # IF THE LENGTH OF ALL FILES == IMAGE COUNTER (A.K.A. NO PHOTOS LEFT)
        if len(all_files) == image_counter:
            # RESET GLOBAL VARIABLES
            image_counter = 0
            add_images_button_count = 0
            max_image = []
            all_files = list()
            # DELETE IMAGES FROM CANVAS
            canvas.delete("all")
            # REDIRECT TO HOME SCREEN
            home_screen()
        # MORE PHOTOS TO PROCESS, BACK TO EDIT SCREEN
        else:
            # CHECK IF EDITED PHOTO EXISTS
            try:
                # DELETE LAST EDITED PHOTO
                os.remove("assets/Edit.jpg")
            # IF IT DOES NOT THEN PASS
            except FileNotFoundError:
                pass
            finally:
                # REDIRECT BACK TO EDIT SCREEN
                edit_screen()


# MAX IMAGE WARNING
def max_image_warning():
    # REFERENCE GLOBAL VARIABLES
    global home_window
    # INITIALIZE POP UP WINDOW
    pop = Toplevel(home_window)
    # SET POP UP WINDOW SIZE
    pop.geometry("300x200")
    # SET POP WINDOW TITLE
    pop.title("Warning")
    # INITIALIZE LABEL TO INFORM USER OF MAX AMOUNT OF IMAGES
    Label(pop, text="Max amount of images reached!").pack(pady=20)
    # CREATE BUTTON TO DESTORY POP UP WINDOW
    Button(pop, text="Understood", command=pop.destroy).pack(pady=40)


# ADD TEXT
def add_text_button():
    # INITIALIZE POP-UP WINDOW
    pop = Toplevel(home_window)
    # SET POP-UP WINDOW SIZE
    pop.geometry("400x375")
    # SET TITLE FOR WINDOW
    pop.title("Add Text")
    # OBTAIN X POSITION
    Label(pop, text="X position:").grid(row=0, column=0, padx=50, pady=25)
    x_text_position = Entry(pop, width=10)
    x_text_position.grid(row=0, column=1)
    # OBTAIN Y POSITION
    Label(pop, text="Y position:").grid(row=1, column=0, padx=25)
    y_text_position = Entry(pop, width=10)
    y_text_position.grid(row=1, column=1)
    # OBTAIN DESIRED TEXT
    Label(pop, text="Text:").grid(row=2, column=0, padx=20, pady=30)
    text = Entry(pop, width=25)
    text.grid(row=2, column=1)
    # OBTAIN DESIRED TEXT COLOR
    # DATATYPE OF MENU TEXT
    variable = StringVar(home_window)
    # DEFAULT VALUE
    variable.set("Black")
    Label(pop, text="Text Color").grid(row=3, column=0)
    text_color = OptionMenu(pop, variable, "Red", "Blue", "Green", "Yellow", "Orange")
    text_color.grid(row=3, column=1)
    # OBTAIN DESIRED FONT SIZE
    # SET SCALE DATATYPE
    v1 = IntVar()
    Label(pop, text="Text Size").grid(row=4, column=0)
    text_size = Scale(pop, variable=v1, from_=1, to=100, orient=HORIZONTAL)
    text_size.grid(row=4, column=1, pady=25)
    # SAVE BUTTON
    save = Button(pop, text="Impose Edits", width=10,
                  command=lambda: add_text_function(pop=pop,
                                                    x_text_position=x_text_position,
                                                    y_text_position=y_text_position,
                                                    text=text,
                                                    text_color=variable,
                                                    text_size=text_size))
    save.grid(row=5, columnspan=3, pady=40)


# ADD TEXT FUNCTION
def add_text_function(pop, x_text_position, y_text_position, text, text_color, text_size):
    # REFERENCE GLOBAL VARIABLES
    global current_image, canvas, image_container
    # TRY TO OPEN EDITED VERSION OF IMAGE
    try:
        # TRY TO OPEN PREVIOUSLY EDITED IMAGE
        current_image = Image.open(fp="assets/Edit.jpg")
        # ENABLE IMAGE EDITING
        draw = ImageDraw.Draw(current_image)
        # CUSTOM FONT SIZE
        myFont = ImageFont.truetype(font="arial.ttf", size=text_size.get())
        # ADD TEXT IMAGE
        draw.text((int(x_text_position.get()), int(y_text_position.get())), text.get(), fill=text_color.get(),
                  font=myFont)
        # CLOSE POP WINDOW
        pop.destroy()
        # SAVE EDITED IMAGE
        current_image.save("assets/Edit.jpg")
        # OPEN AS IMAGE
        current_image = Image.open("assets/Edit.jpg")
        # CONVERT EDITED IMAGE FROM PIL TO TK PHOTO
        current_image = ImageTk.PhotoImage(current_image.resize((500, 400)))
        # UPDATE IMAGE CONTAINER
        canvas.itemconfig(image_container, image=current_image)
    # CATCH INSTANCE WHERE FILE HAS NOT BEEN CREATED YET
    except FileNotFoundError:
        # ENABLE IMAGE EDITING
        draw = ImageDraw.Draw(current_image)
        # CUSTOM FONT SIZE
        myFont = ImageFont.truetype(font="arial.ttf", size=text_size.get())
        # ADD TEXT IMAGE
        draw.text((int(x_text_position.get()), int(y_text_position.get())), text.get(), fill=text_color.get(),
                  font=myFont)
        # CLOSE POP WINDOW
        pop.destroy()
        # SAVE EDITED IMAGE
        current_image.save("assets/Edit.jpg")
        # OPEN AS TK IMAGE
        current_image = Image.open("assets/Edit.jpg")
        # CONVERT EDITED IMAGE FROM PIL TO TK PHOTO THAT IS RESIZED
        current_image = ImageTk.PhotoImage(current_image.resize((500, 400)))
        # UPDATE IMAGE CONTAINER
        canvas.itemconfig(image_container, image=current_image)


# ADD LOGO BUTTON
def add_logo_button():
    # INITIALIZE POP-UP WINDOW
    pop = Toplevel(home_window)
    # SET POP-UP WINDOW SIZE
    pop.geometry("250x200")
    # SET TITLE FOR WINDOW
    pop.title("Add Logo")
    # OBTAIN X POSITION
    Label(pop, text="X position:").grid(row=0, column=0, padx=50, pady=25)
    x_logo_position = Entry(pop, width=10)
    x_logo_position.grid(row=0, column=1)
    # OBTAIN Y POSITION
    Label(pop, text="Y position:").grid(row=1, column=0, padx=25)
    y_logo_position = Entry(pop, width=10)
    y_logo_position.grid(row=1, column=1)
    # OBTAIN DESIRED LOGO
    Button(pop, text="Upload Logo", command=lambda: add_logo_function(x_logo_position=x_logo_position,
                                                                      y_logo_position=y_logo_position)) \
        .grid(row=3, columnspan=3, padx=50, pady=30)


# UPLOAD LOGO
def add_logo_function(x_logo_position, y_logo_position):
    # REFERENCE GLOBAL VARIABLES
    global current_image, canvas, image_container
    # SPECIFY FILE TYPES
    filetypes = [('JPG Files', '*.jpg'), ('PNG Files', '*.png')]
    # OPEN FILE EXPLORER AND ALLOW USER TO SELECT LOGO
    filename = askopenfilename(filetypes=filetypes)
    # OPEN AS IMAGE
    img = Image.open(filename)
    # RESIZE IMAGE
    img = img.resize((200, 200))
    # # TK PHOTO IMAGE
    # img = ImageTk.PhotoImage(img_resized)
    # PASTE LOGO ONTO IMAGE
    current_image.paste(img)
    current_image.save("assets/Edit.jpg")
    # OPEN UPDATED IMAGE
    current_image = Image.open("assets/Edit.jpg")
    # FORMAT OPENED IMAGE TO TK PHOTO IMAGE
    current_image = ImageTk.PhotoImage(current_image.resize((500, 400)))
    # UPDATE CANVAS
    canvas.itemconfig(image_container, image=current_image)


# CLOSE APP
def close_app():
    # REFERENCE GLOBAL VARIABLES
    global home_window, max_image, all_files, add_images_button_count, image_counter
    # TRY TO DELETE EDITED PHOTOS
    try:
        # DELETE EDITED PHOTOS
        os.remove("assets/Edit.jpg")
    # CATCH EXCEPTION FOR NO EDITED PHOTOS EXISTING
    except FileNotFoundError:
        pass
    # RESET GLOBAL VARIABLES AND CLOSE APPLICATION
    finally:
        # RESET ALL FILES
        all_files = []
        max_image = []
        # RESET IMAGE BUTTON COUNT
        add_images_button_count = 0
        # RESET IMAGE COUNTER
        image_counter = 0
        # IF USER DECIDES TO CLOSE APP
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # CLOSE HOME WINDOW
            home_window.destroy()


# RUN HOME SCREEN
home_screen()

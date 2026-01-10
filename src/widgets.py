import customtkinter as ctk
import tkinter.font as tkf
from . import utils 
from . import core
import tkinter.messagebox as tkm

class EntryWidget(ctk.CTkFrame):
    def __init__(self, title: str, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        self.title = title
        self.status = {
            0: "Success",
            1: "Warning",
            2: "Error",
            3: "Info"
        }
        self.status_color = {
            0: "green",
            1: "yellow",
            2: "red",
            3: "turquoise"
        }

        self.entry_height = 290
        self.entry_width = 522
        self.status_width = 522
        self.status_height = 232

        self.entry = ctk.CTkEntry(self, width=self.entry_width, height=self.entry_height, placeholder_text=self.title,
                      font=ctk.CTkFont(size=232))
        self.entry.pack(padx=5, pady=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color=self.status_color[0], width=self.status_width,
                         height=self.status_height, font=ctk.CTkFont(size=185),
                         anchor="w")
        self.status_label.pack(padx=5, pady=5, anchor="se")

    def set_message(self, status: int, message: str):
        self.status_label.configure(text=f"{self.status[status]}: {message}")
        self.status_label.configure(text_color=self.status_color[status])
        self.entry.configure(border_color=self.status_color[status])

    def reset(self):
        self.entry.delete(0, ctk.END)
        self.status_label.configure(text="")
        self.entry.configure(border_color="gray")

class File(ctk.CTkFrame):
    def __init__(self, title: str, timestamp: str, master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        self.title = title
        self.timestamp = timestamp

        self.title_label = ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=15, weight="bold"))
        self.timestamp_label = ctk.CTkLabel(self, text=self.timestamp if self.timestamp else utils.get_timestamp(), font=ctk.CTkFont(size=10))

        self.title_label.place(x=10, y=10)
        self.timestamp_label.place(x=10, y=40)
        

class FileFrame(ctk.CTkFrame):
    def __init__(self, master:ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, heading_font:ctk.CTkFont, body_font:ctk.CTkFont, **kwargs):
        super().__init__(master,**kwargs)
        self.kwargs=kwargs

        self.title = ctk.CTkEntry(self,placeholder_text="Title", width=550, height=heading_font.metrics()["linespace"], font=heading_font)
        self.content = ctk.CTkTextbox(self, width=680, height=kwargs["height"]-heading_font.metrics()["linespace"]-40, font=body_font, wrap="word")
        self.save_button = ctk.CTkButton(self, text="💾", width=50, height=50, font=ctk.CTkFont(size=29))
        self.delete_button = ctk.CTkButton(self, text="❌", width=50, height=50, font=ctk.CTkFont(size=29))

        self.title.place(x=10, y=10)
        self.content.place(x=10, y=heading_font.metrics()["linespace"]+30)
        self.save_button.place(x=570, y=10)
        self.delete_button.place(x=630, y=10)


    def save_note(self,noteid):
        title, content = self.get_data()
        if title == "" and content == "":
            tkm.showerror("New note", "Save the new note by providing a title or content.")
            return
        elif title == "":
            tkm.showwarning("Missing Title", "Please provide a title for the note.")
        elif content == "":
            tkm.showwarning("Missing Content", "Please provide content for the note.")
        else:
            existing = utils.get_file_data(file_id=noteid)
            if existing:
                core.write_note(noteid, content, title)
            else:
                new_id = utils.generate_id()
                core.write_note(new_id, content, title)
            tkm.showinfo("Note Saved", "The note has been saved successfully.")

    def delete_note(self,noteid):
        if tkm.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            core.delete_note(noteid)
            tkm.showinfo("Note Deleted", "The note has been deleted successfully.")
            
    
    def get_data(self):
        return [self.title.get(), self.content.get("1.0", ctk.END).strip()]

    def set_up(self,noteid):
        file_data=utils.get_file_data(file_id=noteid)
        if file_data:
            self.title.delete(0,ctk.END)
            self.title.insert(0,file_data["title"])
            content=core.read_notes(noteid)
            self.content.delete("1.0",ctk.END)
            self.content.insert("1.0",content)
        else:
            self.title.delete(0,ctk.END)
            self.content.delete("1.0",ctk.END)

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master:ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame,header_font:ctk.CTkFont,body_font:ctk.CTkFont, **kwargs):
        super().__init__(master,**kwargs)
        ctk.CTkLabel(self,text="Settings",font=header_font).place(x=10,y=10)

        ctk.CTkLabel(self,text="Theme:",font=body_font,height=body_font.metrics("linespace")).place(x=10,y=body_font.metrics("linespace")+10+header_font.metrics("linespace"))
        self.theme=ctk.CTkOptionMenu(self,values=["light","dark"],font=body_font)
        self.theme.place(x=body_font.measure("Theme:")*1.25,y=(body_font.metrics("linespace")+10)+header_font.metrics("linespace"))

        ctk.CTkLabel(self,text="Color Scheme:",font=body_font,height=body_font.metrics("linespace")).place(x=10,y=(body_font.metrics("linespace")+10)*2+header_font.metrics("linespace"))
        self.color=ctk.CTkOptionMenu(self,values=["blue","green","dark-blue"],font=body_font)
        self.color.place(x=body_font.measure("Color Scheme:")*1.25,y=(body_font.metrics("linespace")+10)*2+header_font.metrics("linespace") )

        ctk.CTkLabel(self,text="Font family:",font=body_font,height=body_font.metrics("linespace")).place(x=10,y=(body_font.metrics("linespace")+10)*3+header_font.metrics("linespace"))
        self.font_family=ctk.CTkOptionMenu(self,values=tkf.families(),font=body_font)
        self.font_family.place(x=body_font.measure("Font family:")*1.25,y=(body_font.metrics("linespace")+10)*3+header_font.metrics("linespace"))

        ctk.CTkLabel(self,text="Heading Font Size:",font=body_font,height=body_font.metrics("linespace")).place(x=10,y=(body_font.metrics("linespace")+10)*4+header_font.metrics("linespace"))
        self.heading_font_size=ctk.CTkSlider(self,from_=35,to=60,number_of_steps=25,width=body_font.measure("Heading Font Size:")+50,
                                             command=self.update_heading_font_label)
        self.heading_font_size.place(x=body_font.measure("Heading Font Size:")*1.25,y=(body_font.metrics("linespace")+10)*4.125+header_font.metrics("linespace"))
        self.heading_font_label=ctk.CTkLabel(self,text=f"{int(self.heading_font_size.get())} pt",font=body_font)
        self.heading_font_label.place(x=(body_font.measure("Heading Font Size:")+10)*2.5,y=(body_font.metrics("linespace")+10)*4+header_font.metrics("linespace"))

        ctk.CTkLabel(self,text="Body Font Size:",font=body_font,height=body_font.metrics("linespace")).place(x=10,y=(body_font.metrics("linespace")+10)*5+header_font.metrics("linespace"))
        self.body_font_size=ctk.CTkSlider(self,from_=18,to=30,number_of_steps=12,width=body_font.measure("Body Font Size:")+50,
                                             command=self.update_body_font_label)
        self.body_font_size.place(x=body_font.measure("Body Font Size:")*1.25,y=(body_font.metrics("linespace")+10)*5.125+header_font.metrics("linespace"))
        self.body_font_label=ctk.CTkLabel(self,text=f"{int(self.body_font_size.get())} pt",font=body_font)
        self.body_font_label.place(x=(body_font.measure("Body Font Size:")+10)*2.5,y=(body_font.metrics("linespace")+10)*5+header_font.metrics("linespace"))
        self.save=ctk.CTkButton(self,text="Save Settings",width=kwargs["width"]-20,height=50,font=body_font)
        self.save.place(relx=0.5,y=kwargs["height"]-40,anchor="center")

    def update_heading_font_label(self,value):
        self.heading_font_label.configure(text=f"{int(value)} pt")

    def update_body_font_label(self,value):
        self.body_font_label.configure(text=f"{int(value)} pt")

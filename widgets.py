import customtkinter as ctk
import tkinter.font as tkf
from functions import get_timestamp, read, write
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
        self.timestamp_label = ctk.CTkLabel(self, text=self.timestamp if self.timestamp else get_timestamp(), font=ctk.CTkFont(size=10))

        self.title_label.place(x=10, y=10)
        self.timestamp_label.place(x=10, y=40)
        

class FileFrame(ctk.CTkFrame):
    def __init__(self, fileid:str, master:ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, heading_font:ctk.CTkFont, body_font:ctk.CTkFont, **kwargs):
        super().__init__(master,**kwargs)
        self.id=fileid
        self.kwargs=kwargs

        self.title = ctk.CTkEntry(self,placeholder_text="Title", width=550, height=heading_font.metrics()["linespace"], font=heading_font)
        self.content = ctk.CTkTextbox(self, width=680, height=kwargs["height"]-heading_font.metrics()["linespace"]-40, font=body_font, wrap="word")
        self.save_button = ctk.CTkButton(self, text="💾", width=50, height=50, font=ctk.CTkFont(size=29))
        self.delete_button = ctk.CTkButton(self, text="❌", width=50, height=50, font=ctk.CTkFont(size=29))

        self.title.place(x=10, y=10)
        self.content.place(x=10, y=heading_font.metrics()["linespace"]+30)
        self.save_button.place(x=570, y=10)
        self.delete_button.place(x=630, y=10)


    def save_note(self,cache):
        for index,note in enumerate(cache["notes"]):
            if note["id"] == self.id:
                title, content = self.get_data()
                if title == "" and content == "":
                    if cache["notes"][index]["title"] == "" and cache["notes"][index]["content"] == "":
                        tkm.showerror("New note", "Save the new note by providing a title or content.")
                        del cache["notes"][index]
                        write(cache)
                    else:
                        tkm.showinfo("Empty Note", "The note must have a title or content to be saved.")
                elif title == "":
                    tkm.showwarning("Missing Title", "Please provide a title for the note.")
                    break
                elif content == "":
                    tkm.showwarning("Missing Content", "Please provide content for the note.")
                    break
                else:
                    cache["notes"][index]["title"] = title
                    cache["notes"][index]["content"] = content
                    cache["notes"][index]["timestamp"] = get_timestamp()
                    write(cache)
                    tkm.showinfo("Note Saved", "The note has been saved successfully.")
                    break
                    


    def delete_note(self,cache):
        if tkm.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            cache["notes"]=[note for note in cache["notes"] if note["id"]!=self.id]
            write(cache)
            tkm.showinfo("Note Deleted", "The note has been deleted successfully.")
        else:
            if self.title.get()=="" and self.content.get("1.0", ctk.END).strip()=="":
                cache["notes"]=[note for note in cache["notes"] if note["id"]!=self.id]
                write(cache)
    
    def get_data(self):
        return [self.title.get(), self.content.get("1.0", ctk.END).strip()]

    def set_up(self, cache):
        self.title.delete(0, ctk.END)
        self.content.delete("1.0", ctk.END) if cache["notes"] else None
        for note in cache["notes"]:
            if note["id"]==self.id:
                self.title.insert(0, note["title"])
                self.title.focus_set()
                self.content.insert("1.0", note["content"])
                break

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

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.load_widgets()
        
    def load_widgets(self):
        for widget in self.children.values():
            widget.destroy()
        self.cache=read()
        self.geometry("800x600")
        self.title("Notebook")
        self.iconbitmap("notepad.ico")
        self.resizable(False,False)
        ctk.set_default_color_theme(self.cache["settings"]["color-scheme"])
        ctk.set_appearance_mode(self.cache["settings"]["theme"])
        self.colormap={
            "blue":"#007BB8",
            "green":"#00A651",
            "dark-blue":"#0057A3",
        }
        self.header_font=ctk.CTkFont(size=self.cache["settings"]["heading-font-size"],family=self.cache["settings"]["font-family"])
        self.body_font=ctk.CTkFont(size=self.cache["settings"]["body-font-size"],family=self.cache["settings"]["font-family"])


        self.side_bar=ctk.CTkFrame(self,width=70,height=580)
        self.side_bar.place(x=10,y=10)

        self.home=ctk.CTkButton(self.side_bar,text="\u2302",width=50,height=50,font=ctk.CTkFont(size=29),command=self.to_home)
        self.home.place(x=10,y=10)
        self.home.configure(state="disabled")

        self.new=ctk.CTkButton(self.side_bar,text="+",width=50,height=50,command=self.new_note,font=ctk.CTkFont(size=29))
        self.new.place(x=10,y=70)

        self.setting=ctk.CTkButton(self.side_bar,text="\u2261",width=50,height=50,font=ctk.CTkFont(size=29),command=self.open_settings)
        self.setting.place(x=10,y=520)

        self.note=ctk.CTkFrame(self,width=700,height=580)
        self.note.place(x=90,y=10)

        self.note_title=ctk.CTkLabel(self.note,text="Notes",font=self.header_font)
        self.note_title.place(x=10,y=10)

        self.scrollframe=ctk.CTkScrollableFrame(self.note,width=690,height=580,bg_color="transparent",fg_color="transparent",border_width=0)
        self.scrollframe.place(x=0,y=90)
        self.scrollframe._scrollbar.configure(width=0)

        self.noteframe=FileFrame(get_timestamp(),self,width=700,height=580,heading_font=self.header_font,body_font=self.body_font)
        self.noteframe.place(x=90,y=10)
        self.noteframe.save_button.configure(command=self.save_note)
        self.noteframe.delete_button.configure(command=lambda:self.noteframe.delete_note(self.cache) or self.to_home())

        self.settings=SettingsFrame(self,width=700,height=580,header_font=self.header_font,body_font=self.body_font)
        self.settings.place(x=90,y=10)
        self.settings.theme.set(self.cache["settings"]["theme"])
        self.settings.theme.configure(command=self.check_settings_state)
        self.settings.color.set(self.cache["settings"]["color-scheme"])
        self.settings.color.configure(command=self.check_settings_state)
        self.settings.font_family.set(self.cache["settings"]["font-family"])
        self.settings.font_family.configure(command=self.check_settings_state)
        self.settings.heading_font_size.set(self.cache["settings"]["heading-font-size"])
        self.settings.heading_font_size.configure(command=lambda value:self.settings.update_heading_font_label(value)
                                                or self.check_settings_state())
        self.settings.body_font_size.set(self.cache["settings"]["body-font-size"])
        self.settings.body_font_size.configure(command=lambda value:self.settings.update_body_font_label(value)
                                               or self.check_settings_state())
        self.settings.heading_font_label.configure(text=f"{self.cache['settings']['heading-font-size']} pt")
        self.settings.body_font_label.configure(text=f"{self.cache['settings']['body-font-size']} pt")
        self.settings.save.configure(command=self.save_settings,state="disabled")
        self.load_notes()
        self.to_home()

    def load_notes(self):
        for widget in self.scrollframe.winfo_children():
            widget.destroy()
        color=self.colormap[self.cache["settings"]["color-scheme"]]
        for note in self.cache.get("notes",[]):
            file_widget=File(note["title"],note["timestamp"],self.scrollframe,height=80,fg_color=color,corner_radius=10,)
            file_widget.pack(padx=10,pady=5,fill="x",)
            file_widget.bind("<Button-1>",lambda event,note_id=note["id"]:self.open_note(note_id))

    def add_note(self):
        new_note={
            "id":get_timestamp(),
            "title":"",
            "content":"",
            "timestamp":get_timestamp()
        }
        self.cache["notes"].append(new_note)
        write(self.cache)

    def open_note(self,note_id):
        self.noteframe.tkraise()
        self.noteframe.id=note_id
        self.noteframe.set_up(self.cache)
        self.setting.configure(state="disabled")

    def new_note(self):
        self.add_note()
        self.open_note(self.cache["notes"][-1]["id"])
        self.home.configure(state="disabled")
        self.new.configure(state="disabled")
        self.setting.configure(state="disabled")

    def save_note(self):
        self.noteframe.save_note(self.cache)
        self.home.configure(state="normal")
        self.new.configure(state="normal")
        self.setting.configure(state="normal")

    def to_home(self):
        self.load_notes()
        self.note.tkraise()
        self.home.configure(state="disabled")
        self.new.configure(state="normal")    
        self.setting.configure(state="normal")

    def open_settings(self):
        self.settings.tkraise()
        self.home.configure(state="normal")
        self.new.configure(state="normal")

    def kill_children(self):
        for child in self.winfo_children():
            child.destroy()

    def save_settings(self):
        self.cache["settings"]["theme"]=self.settings.theme.get()
        self.cache["settings"]["color-scheme"]=self.settings.color.get()
        self.cache["settings"]["font-family"]=self.settings.font_family.get()
        self.cache["settings"]["heading-font-size"]=int(self.settings.heading_font_size.get())
        self.cache["settings"]["body-font-size"]=int(self.settings.body_font_size.get())
        write(self.cache)
        self.kill_children()
        ctk.set_default_color_theme(self.cache["settings"]["color-scheme"])
        ctk.set_appearance_mode(self.cache["settings"]["theme"])
        self.load_widgets()
        self.settings.tkraise()
        self.home.configure(state="normal")
        self.settings.save.configure(state="disabled")

    def check_settings_state(self,event=None):
        state=[
            self.cache["settings"]["theme"]==self.settings.theme.get(),
            self.cache["settings"]["color-scheme"]==self.settings.color.get(),
            self.cache["settings"]["font-family"]==self.settings.font_family.get(),
            self.cache["settings"]["heading-font-size"]==int(self.settings.heading_font_size.get()),
            self.cache["settings"]["body-font-size"]==int(self.settings.body_font_size.get())
        ]
        if all(state):
            self.settings.save.configure(state="disabled")
            self.home.configure(state="disabled")
            self.new.configure(state="disabled")
        else:
            self.settings.save.configure(state="normal")
            self.home.configure(state="normal")
            self.new.configure(state="normal")
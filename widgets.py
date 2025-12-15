import customtkinter as ctk
from functions import get_timestamp, read, write

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
    def __init__(self, fileid:str, master:ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, **kwargs):
        super().__init__(master,**kwargs)
        self.id=fileid
        self.kwargs=kwargs

        self.title = ctk.CTkEntry(self,placeholder_text="Title", width=550, height=50, font=ctk.CTkFont(size=35, weight="bold"))
        self.content = ctk.CTkTextbox(self, width=680, height=500, font=ctk.CTkFont(size=25), wrap="word")
        self.save_button = ctk.CTkButton(self, text="💾", width=50, height=50, font=ctk.CTkFont(size=29))
        self.delete_button = ctk.CTkButton(self, text="❌", width=50, height=50, font=ctk.CTkFont(size=29))

        self.title.place(x=10, y=10)
        self.content.place(x=10, y=70)
        self.save_button.place(x=570, y=10)
        self.delete_button.place(x=630, y=10)


    def save_note(self,cache):
        for note in cache["notes"]:
            if note["id"] == self.id:
                note["title"] = self.title.get()
                note["content"] = self.content.get("1.0", ctk.END).strip()
                note["timestamp"] = get_timestamp()
                break

        write(cache)

    def delete_note(self,cache):
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
    def __init__(self, master:ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, **kwargs):
        super().__init__(master,**kwargs)
        ctk.CTkLabel(self,text="Settings",font=ctk.CTkFont(size=40)).place(x=10,y=10)

        ctk.CTkLabel(self,text="Theme:",font=ctk.CTkFont(size=20)).place(x=10,y=70)
        self.theme=ctk.CTkOptionMenu(self,values=["light","dark"])
        self.theme.place(x=90,y=70)

        ctk.CTkLabel(self,text="Color Scheme:",font=ctk.CTkFont(size=20)).place(x=10,y=110)
        self.color=ctk.CTkOptionMenu(self,values=["blue","green","dark-blue"])
        self.color.place(x=150,y=110)

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
        self.resizable(False,False)
        ctk.set_default_color_theme(self.cache["settings"]["color_scheme"])
        ctk.set_appearance_mode(self.cache["settings"]["theme"])
        self.colormap={
            "blue":"#007BB8",
            "green":"#00A651",
            "dark-blue":"#0057A3",
        }

        self.side_bar=ctk.CTkFrame(self,width=70,height=580)
        self.side_bar.place(x=10,y=10)

        self.home=ctk.CTkButton(self.side_bar,text="\u2302",width=50,height=50,font=ctk.CTkFont(size=29),command=self.to_home)
        self.home.place(x=10,y=10)

        self.new=ctk.CTkButton(self.side_bar,text="+",width=50,height=50,command=self.new_note,font=ctk.CTkFont(size=29))
        self.new.place(x=10,y=70)

        self.settings=ctk.CTkButton(self.side_bar,text="\u2261",width=50,height=50,font=ctk.CTkFont(size=29),command=self.open_settings)
        self.settings.place(x=10,y=520)

        self.note=ctk.CTkFrame(self,width=700,height=580)
        self.note.place(x=90,y=10)

        self.scrollframe=ctk.CTkScrollableFrame(self.note,width=690,height=580,bg_color="transparent",fg_color="transparent",border_width=0)
        self.scrollframe.place(x=0,y=90)
        self.scrollframe._scrollbar.configure(width=0)

        self.noteframe=FileFrame(get_timestamp(),self,width=700,height=580)
        self.noteframe.place(x=90,y=10)
        self.noteframe.save_button.configure(command=self.save_note)
        self.noteframe.delete_button.configure(command=lambda:self.noteframe.delete_note(self.cache) or self.to_home())

        self.settings=SettingsFrame(self,width=700,height=580)
        self.settings.place(x=90,y=10)
        self.settings.theme.configure(command=self.change_theme)
        self.settings.color.configure(command=self.change_color_scheme)
        self.settings.theme.set(self.cache["settings"]["theme"])
        self.settings.color.set(self.cache["settings"]["color_scheme"])

        self.note.tkraise()
        self.load_notes()

    def load_notes(self):
        for widget in self.scrollframe.winfo_children():
            widget.destroy()
        color=self.colormap[self.cache["settings"]["color_scheme"]]
        for note in self.cache.get("notes",[]):
            file_widget=File(note["title"],note["timestamp"],self.scrollframe,height=80,fg_color=color,corner_radius=10)
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

    def new_note(self):
        self.add_note()
        self.open_note(self.cache["notes"][-1]["id"])

    def save_note(self):
        self.noteframe.save_note(self.cache)

    def to_home(self):
        self.load_notes()
        self.note.tkraise()

    def open_settings(self):
        self.settings.tkraise()

    def kill_children(self):
        for child in self.winfo_children():
            child.destroy()

    def change_theme(self,event=None):
        self.cache["settings"]["theme"]=self.settings.theme.get()
        write(self.cache)
        ctk.set_appearance_mode(self.cache["settings"]["theme"])

    def change_color_scheme(self,event=None):
        self.cache["settings"]["color_scheme"]=self.settings.color.get()
        write(self.cache)
        ctk.set_default_color_theme(self.cache["settings"]["color_scheme"])
        self.kill_children()
        self.load_widgets()
        self.settings.tkraise()
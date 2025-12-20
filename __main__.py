import customtkinter as ctk
from widgets import SettingsFrame, FileFrame, File
from functions import get_timestamp, read, write

cache=read()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.load_widgets()
        
    def load_widgets(self):
        for widget in self.children.values():
            widget.destroy()
        self.geometry("800x600")
        self.title("Notebook")
        self.iconbitmap("notepad.ico")
        self.resizable(False,False)
        ctk.set_default_color_theme(cache["settings"]["color-scheme"])
        ctk.set_appearance_mode(cache["settings"]["theme"])
        self.colormap={
            "blue":"#007BB8",
            "green":"#00A651",
            "dark-blue":"#0057A3",
        }
        self.header_font=ctk.CTkFont(size=cache["settings"]["heading-font-size"],family=cache["settings"]["font-family"])
        self.body_font=ctk.CTkFont(size=cache["settings"]["body-font-size"],family=cache["settings"]["font-family"])


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
        self.noteframe.delete_button.configure(command=lambda:self.noteframe.delete_note(cache) or self.to_home())

        self.settings=SettingsFrame(self,width=700,height=580,header_font=self.header_font,body_font=self.body_font)
        self.settings.place(x=90,y=10)
        self.settings.theme.set(cache["settings"]["theme"])
        self.settings.theme.configure(command=self.check_settings_state)
        self.settings.color.set(cache["settings"]["color-scheme"])
        self.settings.color.configure(command=self.check_settings_state)
        self.settings.font_family.set(cache["settings"]["font-family"])
        self.settings.font_family.configure(command=self.check_settings_state)
        self.settings.heading_font_size.set(cache["settings"]["heading-font-size"])
        self.settings.heading_font_size.configure(command=lambda value:self.settings.update_heading_font_label(value)
                                                or self.check_settings_state())
        self.settings.body_font_size.set(cache["settings"]["body-font-size"])
        self.settings.body_font_size.configure(command=lambda value:self.settings.update_body_font_label(value)
                                               or self.check_settings_state())
        self.settings.heading_font_label.configure(text=f"{cache['settings']['heading-font-size']} pt")
        self.settings.body_font_label.configure(text=f"{cache['settings']['body-font-size']} pt")
        self.settings.save.configure(command=self.save_settings,state="disabled")
        self.load_notes()
        self.to_home()

    def load_notes(self):
        for widget in self.scrollframe.winfo_children():
            widget.destroy()
        color=self.colormap[cache["settings"]["color-scheme"]]
        for note in cache.get("notes",[]):
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
        cache["notes"].append(new_note)
        write(cache)

    def open_note(self,note_id):
        self.noteframe.tkraise()
        self.noteframe.id=note_id
        self.noteframe.set_up(cache)
        self.setting.configure(state="disabled")

    def new_note(self):
        self.add_note()
        self.open_note(cache["notes"][-1]["id"])
        self.home.configure(state="disabled")
        self.new.configure(state="disabled")
        self.setting.configure(state="disabled")

    def save_note(self):
        self.noteframe.save_note(cache)
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
        cache["settings"]["theme"]=self.settings.theme.get()
        cache["settings"]["color-scheme"]=self.settings.color.get()
        cache["settings"]["font-family"]=self.settings.font_family.get()
        cache["settings"]["heading-font-size"]=int(self.settings.heading_font_size.get())
        cache["settings"]["body-font-size"]=int(self.settings.body_font_size.get())
        write(cache)
        self.kill_children()
        ctk.set_default_color_theme(cache["settings"]["color-scheme"])
        ctk.set_appearance_mode(cache["settings"]["theme"])
        self.load_widgets()
        self.settings.tkraise()
        self.home.configure(state="normal")
        self.settings.save.configure(state="disabled")

    def check_settings_state(self,event=None):
        state=[
            cache["settings"]["theme"]==self.settings.theme.get(),
            cache["settings"]["color-scheme"]==self.settings.color.get(),
            cache["settings"]["font-family"]==self.settings.font_family.get(),
            cache["settings"]["heading-font-size"]==int(self.settings.heading_font_size.get()),
            cache["settings"]["body-font-size"]==int(self.settings.body_font_size.get())
        ]
        if all(state):
            self.settings.save.configure(state="disabled")
            self.home.configure(state="disabled")
            self.new.configure(state="disabled")
        else:
            self.settings.save.configure(state="normal")
            self.home.configure(state="normal")
            self.new.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
        
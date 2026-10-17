
import tkinter as tk
import random
from PIL import Image, ImageTk


# COLORS
BACKGROUND = "#1B102B"
PANEL = "#302044"
PURPLE = "#A970FF"
WHITE = "#FFFFFF"
BTN_BG = "#69428A"


class ShopGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Piksi's Shop")
        self.root.geometry("850x650")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)

        self.selected_food_index = None
        self.current_page = 0

        # FOOD DATA
        self.foods = [
            {
                "name": "Onigiri",
                "file": "Food1-removebg-preview.png",
                "bought": False
            },
            {
                "name": "Minecraft cake?",
                "file": "Food2-removebg-preview.png",
                "bought": False
            },
            {
                "name": "Candy",
                "file": "Food3-removebg-preview.png",
                "bought": False
            },
            {
                "name": "Cupcake",
                "file": "Food4-removebg-preview.png",
                "bought": False
            },
            {
                "name": "Cake",
                "file": "Food5-removebg-preview.png",
                "bought": False
            },
            {
                "name": "Pudding",
                "file": "Food6-removebg-preview.png",
                "bought": False
            },
        ]

        # REACTION FILES
        self.reaction_files = {
            1: "Reaction1Org-removebg-preview.png",
            2: "Reaction2New-removebg-preview.png",
            3: "Reaction3New-removebg-preview.png",
            4: "Reaction4New-removebg-preview.png",
            5: "Reaction5New-removebg-preview.png",
            6: "Reaction6New-removebg-preview.png",
        }

        try:
            self.load_images()
        except (FileNotFoundError, OSError) as error:
            message = (
                f"Could not load an image:\n\n{error}\n\n"
                "Check that all image files are in the same "
                "folder as this Python file."
            )
            tk.messagebox.showerror("Image error", message)
            self.root.destroy()
            return

        self.create_widgets()

        self.set_reaction(1)
        self.show_dialog(
            "Piksi: Hi! Welcome to my sweet shop!"
        )

    # LOAD IMAGES
    def load_images(self):
        # Background
        bg = Image.open("Bg.jpg").convert("RGB")
        bg = bg.resize((850, 650), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(bg)

        # Piksi reactions
        self.reactions = {}

        for number, filename in self.reaction_files.items():
            img = Image.open(filename).convert("RGBA")

            # Bigger character
            img.thumbnail((500, 510), Image.Resampling.LANCZOS)

            self.reactions[number] = ImageTk.PhotoImage(img)

        # Food images
        self.food_images = []

        for food in self.foods:
            img = Image.open(food["file"]).convert("RGBA")
            img.thumbnail((100, 100), Image.Resampling.LANCZOS)

            self.food_images.append(ImageTk.PhotoImage(img))

    # CREATE INTERFACE
    def create_widgets(self):
        self.canvas = tk.Canvas(
            self.root,
            width=850,
            height=650,
            bg=BACKGROUND,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Background image
        self.canvas.create_image(
            0, 0,
            image=self.bg_img,
            anchor="nw"
        )

        # Piksi directly on Canvas.
        # Transparent PNG pixels reveal the background.
        self.piksi_image_id = self.canvas.create_image(
            35, 40,
            image=self.reactions[1],
            anchor="nw",
            tags="piksi"
        )

        self.canvas.tag_bind(
            "piksi",
            "<Button-1>",
            lambda event: self.click_piksi()
        )

        # SHOP
        self.shop_frame = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        self.canvas.create_window(
            580, 25,
            anchor="nw",
            window=self.shop_frame
        )

        self.food_slots = []

        for i in range(3):
            frame = tk.Frame(
                self.shop_frame,
                bg=BACKGROUND
            )
            frame.pack(pady=5)

            btn = tk.Button(
                frame,
                bg=BACKGROUND,
                activebackground=BACKGROUND,
                bd=0,
                highlightthickness=0,
                relief="flat",
                cursor="hand2"
            )
            btn.pack()

            lbl = tk.Label(
                frame,
                text="",
                font=("Arial", 9, "bold"),
                bg=BACKGROUND,
                fg=WHITE
            )
            lbl.pack()

            self.food_slots.append((btn, lbl))

        # Page button
        self.page_btn = tk.Button(
            self.shop_frame,
            text="➡️ Next Page",
            font=("Arial", 10, "bold"),
            bg=PURPLE,
            fg=WHITE,
            activebackground=BTN_BG,
            relief="flat",
            cursor="hand2",
            command=self.toggle_page
        )
        self.page_btn.pack(pady=5)

        # DIALOGUE
        self.dialog_frame = tk.Frame(
            self.root,
            bg=PANEL,
            highlightbackground=PURPLE,
            highlightthickness=2
        )

        self.canvas.create_window(
            40, 480,
            anchor="nw",
            window=self.dialog_frame,
            width=770,
            height=140
        )

        self.dialog_text = tk.Label(
            self.dialog_frame,
            text="",
            font=("Arial", 12, "bold"),
            fg=WHITE,
            bg=PANEL,
            wraplength=740,
            justify="left",
            anchor="nw"
        )
        self.dialog_text.pack(
            padx=15,
            pady=10,
            anchor="nw"
        )

        self.buttons_frame = tk.Frame(
            self.dialog_frame,
            bg=PANEL
        )
        self.buttons_frame.pack(
            padx=10,
            pady=5,
            anchor="sw",
            fill="x"
        )

        self.update_food_display()

    # UPDATE SHOP
    def update_food_display(self):
        start_idx = self.current_page * 3

        for i in range(3):
            idx = start_idx + i
            btn, lbl = self.food_slots[i]

            if idx < len(self.foods):
                food = self.foods[idx]

                btn.config(
                    image=self.food_images[idx],
                    command=lambda item_idx=idx:
                        self.click_food(item_idx)
                )

                if food["bought"]:
                    lbl.config(
                        text="[ SOLD OUT ]",
                        fg="#FF5555"
                    )
                else:
                    lbl.config(
                        text=food["name"],
                        fg=WHITE
                    )

                btn.pack()
                lbl.pack()
            else:
                btn.pack_forget()
                lbl.pack_forget()

    def toggle_page(self):
        self.current_page = 1 if self.current_page == 0 else 0

        if self.current_page == 1:
            self.page_btn.config(text="⬅️ Previous Page")
        else:
            self.page_btn.config(text="➡️ Next Page")

        self.update_food_display()

    # REACTIONS
    def set_reaction(self, number):
        self.canvas.itemconfig(
            self.piksi_image_id,
            image=self.reactions[number]
        )

    # DIALOGUES
    def show_dialog(self, text, buttons_data=None):
        self.dialog_text.config(text=text)

        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        if buttons_data:
            for btn_text, cmd in buttons_data:
                button = tk.Button(
                    self.buttons_frame,
                    text=btn_text,
                    font=("Arial", 10, "bold"),
                    bg=PURPLE,
                    fg=WHITE,
                    activebackground=BTN_BG,
                    relief="flat",
                    cursor="hand2",
                    command=cmd
                )
                button.pack(side="left", padx=5)

    def clear_dialog_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        self.set_reaction(3)

    # BUY FOOD
    def click_food(self, index):
        self.selected_food_index = index
        food = self.foods[index]

        if food["bought"]:
            self.set_reaction(2)

            self.show_dialog(
                "Piksi: ...?\n"
                "You already bought this, why are you doing this? "
                "Didn't you already buy it?",
                [("Got it", self.clear_dialog_buttons)]
            )
        else:
            self.set_reaction(3)

            self.show_dialog(
                f"Do you want to buy '{food['name']}'?",
                [
                    ("Yes", self.buy_food),
                    ("No", self.clear_dialog_buttons)
                ]
            )

    def buy_food(self):
        if self.selected_food_index is None:
            return

        idx = self.selected_food_index

        if self.foods[idx]["bought"]:
            return

        self.foods[idx]["bought"] = True
        self.update_food_display()

        all_bought = all(
            food["bought"] for food in self.foods
        )

        if all_bought:
            self.set_reaction(5)

            self.show_dialog(
                "Piksi: I'm glad you liked it!",
                [("Next", self.end_game)]
            )

        elif random.choice([True, False]):
            self.set_reaction(6)

            self.show_dialog(
                "Piksi: Thank you for your purchase!",
                [("Thank you too!", self.thank_piksi)]
            )

        else:
            self.set_reaction(3)

            self.show_dialog(
                "Purchase successful!",
                [("OK", self.clear_dialog_buttons)]
            )

    def thank_piksi(self):
        self.set_reaction(5)

        self.show_dialog(
            "Piksi: I'm glad you liked it!",
            [("OK", self.clear_dialog_buttons)]
        )

    # TALK TO PIKSI
    def click_piksi(self):
        self.set_reaction(4)

        self.show_dialog(
            "Piksi: What do you want?",
            [
                ("Ask something", self.ask_piksi_menu),
                ("Ask for free food", self.ask_free)
            ]
        )

    def ask_piksi_menu(self):
        self.set_reaction(4)

        self.show_dialog(
            "Piksi: What do you want to ask?",
            [
                ("Can I buy anything else?", self.answer_more),
                ("Is there anything besides this?", self.answer_other),
                ("Back", self.clear_dialog_buttons)
            ]
        )

    def answer_more(self):
        self.set_reaction(4)

        self.show_dialog(
            "Piksi: Unfortunately no, everything else "
            "is still being prepared.",
            [("Got it", self.clear_dialog_buttons)]
        )

    def answer_other(self):
        self.set_reaction(4)

        self.show_dialog(
            "Piksi: For now, there's only this.",
            [("Got it", self.clear_dialog_buttons)]
        )

    def ask_free(self):
        self.set_reaction(2)

        self.show_dialog(
            "Piksi: Hey! Nothing is given for free!",
            [("Okay...", self.clear_dialog_buttons)]
        )

    # END GAME
    def end_game(self):
        self.set_reaction(1)

        self.show_dialog(
            "Piksi: Wow, you bought absolutely everything! "
            "Thank you so much for visiting! See you soon!",
            [("Finish Game", self.root.destroy)]
        )


# START GAME
if __name__ == "__main__":
    root = tk.Tk()
    app = ShopGame(root)
    root.mainloop()

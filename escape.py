import tkinter as tk
from tkinter import font
from functools import partial


class GameScreen():
    def __init__(self, master, image, roi, inventory_item=None, help_text=None, required_item=None):
        self.master = master
        self.roi = roi
        self.image = tk.PhotoImage(file=image)
        self.inventory_item = inventory_item
        self.help_text = help_text
        self.required_item = required_item

    def on_click(self, event, item_in_use):
        if self.master.has_won:
        	return

        if item_in_use and not self.required_item:
        	self.master.show_cannot_use_message()  # mensagem que o jogador não pode usar qaquele item
        elif self.roi[0] <= event.x <= self.roi[2] and self.roi[1] <= event.y <= self.roi[3]:
            if self.inventory_item:
                self.master.add_inventory_item(self.inventory_item)
            if self.required_item:
            	if item_in_use == self.required.item:
            	    self.master.show_next_screen()
            else:
            	self.master.show_next_screen()
        else:
        	if item_in_use:
        		self.master.show_cannot_use_message()


class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        # Atributos:
        self.inventory_slots = []
        self.inventory_slots_in_use = []
        self.current_screen_number = 0
        self.sucess_font = font.Font(family="ubuntu", size=50, weight=font.BOLD)
        self.cannot_use_font = font.Font(family="ubuntu", size=28, weight=font.BOLD)
        self.item_in_use = ""
        self.has_won = False

        self.title("Fuja do Castelo!")
        self.geometry("940x640")
        self.resizable(False, False)

        self.key_image = tk.PhotoImage(file="assets/key.png")
        self.question_mark_image = tk.PhotoImage(file="assets/questionmark2.png")

        self.screen = tk.Canvas(self, bg="white", width=940, height=800)
        self.right_frame = tk.Frame(self, width=300, height=800)
        self.right_frame.pack_propagate(0)

        self.help_var = tk.StringVar(self.right_frame)
        self.help_var.set("Tente clicar em algo.")

        self.help_box = tk.Label(self.right_frame, textvar=self.help_var, background="black", foreground="white",
                                 padx=10, pady=20)
        self.help_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        inventory_title = tk.Label(self.right_frame, text="Inventário: ", background="grey", foreground="white")

        inventory_space = tk.Frame(self.right_frame, background="lightgrey", width=300, height=320)
        inventory_space.pack_propagate(0)

        inventory_space.pack(side=tk.BOTTOM)
        inventory_title.pack(side=tk.BOTTOM, fill=tk.X)

        # colocando as imagens dentro de cada variável de inventário:
        inventory_slot_1 = tk.Button(inventory_space, image=self.question_mark_image, width=50, height=50)
        inventory_slot_2 = tk.Button(inventory_space, image=self.question_mark_image, width=50, height=50)
        inventory_slot_3 = tk.Button(inventory_space, image=self.question_mark_image, width=50, height=50)
         
        # criando um espaço entre os botões de inventário
        inventory_slot_1.pack(pady=(40, 20), padx=20)
        inventory_slot_2.pack(pady=20, padx=20)
        inventory_slot_3.pack(pady=(20, 0), padx=20)

        # inserindo na Lista de inventários os itens (variáveis de inventário):
        self.inventory_slots.append(inventory_slot_1)
        self.inventory_slots.append(inventory_slot_2)
        self.inventory_slots.append(inventory_slot_3)


        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

        # vinculando um método ao clicar na imagem principal:
        self.screen.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        self.active_screen.on_click(event)

    # simplemente seta uma lista de objetos GameScreen como referência da claase Game para criar as telas do jogo:
    def set_game_screens(self, game_screens):
        self.game_screens = game_screens

    def display_screen(self, game_screen_number):
        self.active_screen = self.game_screens[game_screen_number]
        self.screen.delete("all")
        self.screen.create_image((250, 400), image=self.active_screen.image)
        self.help_var.set(self.active_screen.help_text)

    def show_next_screen(self):
        self.current_screen_number += 1;
        if self.current_screen_number < len(self.game_screens):
            self.display_screen(self.current_screen_number)
        else:
            self.screen.delete("all")
            self.screen.configure(bg="black")
            self.screen.create_text((320, 300), text="Você venceu!!", font=self.sucess_font, fill="white")

    def add_inventory_item(self, item_name):
        next_available_inventory_slot = len(self.inventory_slots_in_use)
        if next_available_inventory_slot < len(self.inventory_slots):
            next_slot = self.inventory_slots[next_available_inventory_slot]

            if item_name == "key":
                next_slot.configure(image=self.key_image)

            self.inventory_slots_in_use.append(item_name)

    def play(self):
        if not self.game_screens:
            print("Nenhuma tela adicionada")
        else:
            self.display_screen(0)


if __name__ == "__main__":
    game = Game()

    scene1 = GameScreen(game, "assets/bedroom1.png", (378, 135, 427, 217), "key", "Você tem que sair, "
                                                                                "mas a porta está fechada!\n Encontre a chave.")
    scene2 = GameScreen(game, "assets/scene2.png", (117, 54, 329, 412), None, "Você tem a chave!")
    scene3 = GameScreen(game, "assets/scene3.png", (117, 54, 329, 412), None, "A porta está aberta.")

    all_screens = [scene1, scene2, scene3]

    game.set_game_screens(all_screens)
    game.play()
    game.mainloop()

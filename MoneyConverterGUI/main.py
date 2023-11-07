"""
Money converter app with GUI that 
gathers data from webscraping x-rates.com
"""

from bs4 import BeautifulSoup as bs
import requests
import customtkinter as ctk
from tkinter import messagebox
from time import time

currency_dict = {  # dict of currency names {"US Dollar": "USD", ...}
        "US Dollar": "USD",
        "Argentine Peso": "ARS",
        "Australian Dollar": "AUD",
        "Bahraini Dinar": "BHD",
        "Botswana Pula": "BWP",
        "Brazilian Real": "BRL",
        "Bruneian Dollar": "BND",
        "Bulgarian Lev": "BGN",
        "Canadian Dollar": "CAD",
        "Chilean Peso": "CLP",
        "Chinese Yuan Renminbi": "CNY",
        "Colombian Peso": "COP",
        "Croatian Kuna": "HRK",
        "Czech Koruna": "CZK",
        "Danish Krone": "DKK",
        "Euro": "EUR",
        "Hong Kong Dollar": "HKD",
        "Hungarian Forint": "HUF",
        "Icelandic Krona": "ISK",
        "Indian Rupee": "INR",
        "Indonesian Rupiah": "IDR",
        "Iranian Rial": "IRR",
        "Israeli Shekel": "ILS",
        "Japanese Yen": "JPY",
        "Kazakhstani Tenge": "KZT",
        "South Korean Won": "KRW",
        "Kuwaiti Dinar": "KWD",
        "Libyan Dinar": "LYD",
        "Malaysian Ringgit": "MYR",
        "Mauritian Rupee": "MUR",
        "Mexican Peso": "MXN",
        "Nepalese Rupee": "NPR",
        "New Zealand Dollar": "NZD",
        "Norwegian Krone": "NOK",
        "Omani Rial": "OMR",
        "Pakistani Rupee": "PKR",
        "Philippine Peso": "PHP",
        "Polish Zloty": "PLN",
        "Qatari Riyal": "QAR",
        "Romanian New Leu": "RON",
        "Russian Ruble": "RUB",
        "Saudi Arabian Riyal": "SAR",
        "Singapore Dollar": "SGD",
        "South African Rand": "ZAR",
        "Sri Lankan Rupee": "LKR",
        "Swedish Krona": "SEK",
        "Swiss Franc": "CHF",
        "Taiwan New Dollar": "TWD",
        "Thai Baht": "THB",
        "Trinidadian Dollar": "TTD",
        "Turkish Lira": "TRY",
        "Emirati Dirham": "AED",
        "British Pound": "GBP",
        "Venezuelan Bolivar": "VEF"
    }
dict_keys = list(currency_dict.keys()) # list of currency full names

class App():
    
    def __init__(self):
        # Window setup
        self.root = ctk.CTk() # sets root (MUST ALWAYS SET!!!)
        self.root.geometry("600x300") # sets window size
        self.screen_height = self.root.winfo_screenheight()
        print(self.screen_height)
        self.screen_width = self.root.winfo_screenwidth()
        print(self.screen_width)
        self.root.title("Currency Converter") # sets window name
        
        # Misc Variables 
        self.run_count = 0
        
        # Frame setup
        self.mainframe = ctk.CTkFrame(self.root) # makes a frame object, have to specify parent in ()
        self.mainframe.pack(fill='both', expand=True) # places frame object
        self.mainframe.grid_columnconfigure((0, 1, 2), weight=1, uniform="column") # configures columns in frame
        self.mainframe.grid_rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="row") # configures columns in frame
        

        # Appearance
        ctk.set_appearance_mode("System") # sets window appearance mode ("dark" or "light")
        ctk.set_default_color_theme("green") # sets window color theme


        if self.run_count > 0: # 
            self.arrow = ctk.CTkLabel(self.mainframe, text="--->", font=("", 20))
            self.arrow.grid(row=1, column=1, columnspan=1, sticky="EW")
            
        # Cbox for input currency
        self.combo_inp = ctk.CTkComboBox(self.mainframe, # creates a drop down box with text values object
                                    state="readonly",
                                    values = dict_keys, # what list is used for the dropdown
                                    justify="center",
                                    command= self.update_left_abv, # option 
                                    width=200
                                    )
        self.combo_inp.grid(row = 0, column=0, columnspan=1, padx=10)
        

        # Cbox for ouput currency
        self.combo_out = ctk.CTkComboBox(self.mainframe, # makes a drop down box for right side output currency
                                    state="readonly", 
                                    values = dict_keys,
                                    justify="center",
                                    command= self.update_right_abv,
                                    width=200
                                    )
        self.combo_out.grid(row=0, column=2, columnspan=1, padx=10)
        #self.combo_out.bind("<<ComboboxSelected>>", self.update_arrow)
        

        # User Entry field
        self.entry = ctk.CTkEntry(self.mainframe, justify="center")
        self.entry.grid(row=2, column=1, columnspan=1, sticky="EW")


        # Button to Execute Conversion
        self.button = ctk.CTkButton(self.mainframe, 
                                             text="Convert", 
                                             command = lambda: self.convert(currency_dict[self.left_choice], currency_dict[self.right_choice], self.getEntry()),
                                             hover_color=("light green", "green"),
                                             )
        self.button.grid(row=3, column=1, columnspan=1, sticky="EW")

        def on_closing(): 
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        self.root.mainloop()
        return

    ###### end of __init__() ########

    def update_left_abv(self, choice): # updates inp side abbreviation text
            self.left_label = ctk.CTkLabel(self.mainframe, text=currency_dict[choice], font=("", 20))
            self.left_label.grid(row=1, column=0, columnspan=1, padx=1)  # Input currency dropdown box
            self.left_choice = choice
    
    def update_right_abv(self, choice): # updates out side abbreviation text
            self.right_label = ctk.CTkLabel(self.mainframe, text=currency_dict[choice], font=("", 20))
            self.right_label.grid(row=1, column=2, columnspan=1, padx=1)  # Input currency dropdown box
            self.right_choice = choice

    def getEntry(self): # ensures entry and both dropdowns aren't empty, returns currency value if true
        if self.combo_inp.get() == "" or self.combo_out.get() == "":
            self.open_popup("ERROR: MUST SELECT CURRENCY")
        
        try:
             return(float(self.entry.get()))
        except:
             self.open_popup("ERROR: MUST ENTER VALID VALUE")
    
    def convert(self, inp, out, num): # scrapes x-rates.com for currency conversion and displays converted value
        print(inp, out, num)


        url = (f"https://www.x-rates.com/calculator/?from={inp}&to={out}&amount={num}")
        try: 
            content = requests.get(url, timeout=1).text

        # request exceptions
        except TimeoutError: # if it takes more than 1 sec to load site
            self.open_popup('ERROR: CONNECTION TIMED OUT')
        except ConnectionError: # if connection to site fails
            self.open_popup('ERROR: CONNECTION ERROR')
        
        else: # runs if try is successful 

            # webscraping, finds value in HTML class that result is held
            soup = bs(content, "html.parser")
            result = soup.find("span", class_="ccOutputRslt").getText()
            result = result[0:-6]

            # shows result on screen
            self.answer = ctk.CTkLabel(self.mainframe, text=f"{num} {inp} is {result} {out}",  font=("", 15))
            self.answer.grid(row=4, column=1, columnspan=1, sticky="EW")

            # shows arrow in center
            self.arrow = ctk.CTkLabel(self.mainframe, text=" ---> ", font=("", 20))
            self.arrow.grid(row=1, column=1, columnspan=1, sticky="EW")

            # counts times converter ran during instance, potentially used for animation???
            self.run_count += 1
            

    def open_popup(self, error): # opens a popup for exception error
            self.popup = ctk.CTkToplevel(self.root)
            self.popup.geometry("400x100")
            self.popup.title("QUIT")
            self.popup_label = ctk.CTkLabel(self.popup, text=error, font=("Pixeltype.ttf", 20))
            self.popup_label.pack(pady=10)
            self.popup_button = ctk.CTkButton(self.popup, 
                              text="Okay", 
                              command=self.popup.destroy,
                              #height=40,
                              #width=60
                              )
            self.popup_button.pack(pady=10)
            

def main():
    App()
    
if __name__ == "__main__":
    main()


# Money Converter

### A currency conversion tool with a customtkinter GUI that uses x-rates.com to provide accurate and up-to-date conversion information.

## Usage
- Select the currency to convert from on the left-hand side drop-down.

- Select the currency to convert to on the right-hand side

- Press the "Convert" button to execute currency conversion

- Currency conversion is displayed below the button

## How it works
1) Uses beautifulsoup to go to the x-rates.com URL of the selected currency values and monetary amount
    - The URL format of x-rates.com allows for this
2) The conversion is automatically done from the URL entry
3) Uses beautifulsoup to scrape and return conversion amount
- The GUI was created with [customtkinter](https://customtkinter.tomschimansky.com/), a modern-looking UI library based on tkinter

## Screenshots
- #### Before Execution:
  ![Before Execution](/MoneyConverterGUI/screenshots/beforeentry.png?raw=True)

- #### After Execution:
  ![After Execution](/MoneyConverterGUI/screenshots/afterentry.png?raw=True)
\
\
*Note: This was created recreationally to practice using GUIs and web scraping. It is not intended to be released or distributed beyond means of archiving or professional development.*

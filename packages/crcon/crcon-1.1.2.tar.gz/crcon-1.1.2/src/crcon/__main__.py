import sys
from chromaconsole import Color,Style
from . import check_ver

def print_help():
    help_text = f'''
    {Style.bold()}Usage:{Style.reset()} 
        {Color.text("#ff8")}crcon{Color.default_text()} <command> <color_code or reset>
    
    {Style.bold()}Commands:{Style.reset()}
        text <color_code>    {Color.text("#6c0")}# Set the text color (e.g. #ff0000 for red){Color.default_text()}
        bg <color_code>      {Color.text("#6c0")}# Set the background color{Color.default_text()}
        text reset           {Color.text("#f90")}# Reset the text color{Color.default_text()}
        bg reset             {Color.text("#f90")}# Reset the background color{Color.default_text()}
        style <style>        {Color.text("#6c0")}# Apply a style 
        {Color.text("#bf0")}(italic, bold, doubleunderlined, faint, hidden, normalintensity, overlined, propspacing, reverse, strikethrough, underline){Color.default_text()}

    {Style.bold()}Examples:{Style.reset()}
        {Color.text("#ff8")}crcon{Color.default_text()} text #ff00ff   {Color.text("#6c0")}# Sets the text color to purple{Color.default_text()}
        {Color.text("#ff8")}crcon{Color.default_text()} bg #00ffff     {Color.text("#6c0")}# Sets the background color to aqua{Color.default_text()}
        {Color.text("#ff8")}crcon{Color.default_text()} text reset     {Color.text("#f90")}# Resets the text color to default{Color.default_text()}
        {Color.text("#ff8")}crcon{Color.default_text()} bg reset       {Color.text("#f90")}# Resets the background color to default{Color.default_text()}
        {Color.text("#ff8")}crcon{Color.default_text()} style italic   {Color.text("#6c0")}# Applies italic style{Color.default_text()}
        {Color.text("#ff8")}crcon{Color.default_text()} style bold     {Color.text("#6c0")}# Applies bold style{Color.default_text()}
    '''
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    if sys.argv[1].lower() == "text":
        if len(sys.argv) == 3:
            color_code = sys.argv[2]
            if color_code == "reset":
                print(Color.default_text(), end="")
            else:
                print(Color.text(str(color_code)), end="")
        else:
            print_help()

    elif sys.argv[1].lower() == "bg":
        if len(sys.argv) == 3:
            color_code = sys.argv[2]
            if color_code == "reset":
                print(Color.default_background(), end="")
            else:
                print(Color.background(str(color_code)), end="")
        else:
            print_help()

    elif sys.argv[1].lower() == "style":
        if len(sys.argv) == 3:
            color_code = sys.argv[2]
            if color_code == "italic":
                print(Style.italic(), end="")
            elif color_code == "bold":
                print(Style.bold(), end="")
            elif color_code == "doubleunderlined":
                print(Style.doubly_underlined(), end="")
            elif color_code == "faint":
                print(Style.faint(), end="")
            elif color_code == "hidden":
                print(Style.hidden(), end="")
            elif color_code == "normalintensity":
                print(Style.normal_intensity(), end="")
            elif color_code == "overlined":
                print(Style.overlined(), end="")
            elif color_code == "propspacing":
                print(Style.proportional_spacing(), end="")
            elif color_code == "rapidblink":
                print(Style.rapid_blink(), end="")
            elif color_code == "reveal":
                print(Style.reveal(), end="")
            elif color_code == "reverse":
                print(Style.reverse(), end="")
            elif color_code == "slowblink":
                print(Style.slow_blink(), end="")
            elif color_code == "strikethrough":
                print(Style.strikethrough(), end="")
            elif color_code == "underlined":
                print(Style.underlined(), end="")
            elif color_code == "reset":
                print(Style.reset(), end="")
            else:
                print_help()
        else:
            print_help()
    else:
        print_help()

if __name__ == "__main__":
    check_ver()
    main()
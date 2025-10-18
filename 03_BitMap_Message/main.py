bitmap = """
....................................................................
   **************   *  *** **  *      ******************************
  ********************* ** ** *  * ****************************** *
 **      *****************       ******************************
          *************          **  * **** ** ************** *
           *********            *******   **************** * *
            ********           ***************************  *
   *        * **** ***         *************** ******  ** *
               ****  *         ***************   *** ***  *
                 ******         *************    **   **  *
                 ********        *************    *  ** ***
                   ********         ********          * *** ****
                   *********         ******  *        **** ** * **
                   *********         ****** * *           *** *   *
                     ******          ***** **             *****   *
                     *****            **** *            ********
                    *****             ****              *********
                    ****              **                 *******   *
                    ***                                       *    *
                    **     *                    *
...................................................................."""

import sys

# (!) Try changing this multiline string to any image you like:

# There are 68 periods along the top and bottom of this string:

from colorama import Fore, Back, Style
import time


message=input('Enter message to shpw on bitmap> ')
color=input('Choose color in which you want to show the map: (red,cyan,white,blue,yellow,magenta,green) > ').lower()

color_map={
 "red":Fore.RED,
 "green":Fore.GREEN,
 "blue":Fore.BLUE,
 "yellow":Fore.YELLOW,
 "cyan":Fore.CYAN,
 "magenta":Fore.MAGENTA,
 "white":Fore.WHITE

}


color_choice = color_map.get(color, Fore.CYAN)

if(message==''):
  sys.exit()


final_out=""  

for line in bitmap.splitlines():
    for i,c in enumerate(line):
        
        if(c==' '):
          print(' ', end='') 
          final_out += " "

        else:
          ch = message[i % len(message)]
          print(color_choice + ch, end="")
          final_out += ch
          time.sleep(0.01)
    print()
    final_out += "\n"


with open("output.txt","w") as file:
   file.write(final_out)

print(Style.RESET_ALL + "\n\n Bitmap text art saved to 'output.txt'")
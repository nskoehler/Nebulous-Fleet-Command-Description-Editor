# Nebulous-Fleet-Command-Description-Editor
This is the official repository for the Nebulous: Fleet Command Text Editor

The Nebulous Fleet Command Description Editor is a Text Editor designed for use with the game Nebulous: Fleet Command. It allows you to input text with different colors, sizes and typographs, exporting them in a manner that can simply be copy pasted into the .fleet file of one's choice between the < FactionKey > and < SortOverrideOrder > tags at the start of file (usually at lines 6-7 respectively).

You need python to run the files, and to run the editor properly ensure you initialize from NDE_Main.py specifically.

There are two ways to install and run this code. For those who use VS Code:
1. Ensure you have VS Code and Python installed, and make sure VS Code has Python installed as well as an extension.
2. Download this code from github.
3. From VS Code, open the NDE_Main.py and run the file.
4. The file should run from there. Once you get the output, you can open the fleet file using VS Code or another text editor and add the description to the fleet file using the instructions provided in the editor.
   (If you have Python you can skip the VS Code part by just opening the NDE_Main.py using python.)

If you are a user who does not use VS Code, you can alternatively do the following:
1. Clone the repository by typing the following into the command prompt (ensure you have Python installed):
   git clone https://github.com/nskoehler/Nebulous-Fleet-Command-Description-Editor.git
   cd Nebulous-Fleet-Command-Description-Editor
2. Once installed, you can run the .py file by double clicking it in the files location, or alternatively if you open windows terminal, you can use this to run from the terminal:
   cd path\to\Nebulous-Fleet-Command-Description-Editor
   python NDE_Main.py

   (If you are a macOS/Linux user, type in this instead):
   cd /path/to/Nebulous-Fleet-Command-Description-Editor
   python3 NDE_Main.py
3. Once you have the translated output, you can open the fleet file in text editor (instructions on location in the program itself) and paste the code in there. It should then run in the game.

To test whether or not the editor functions properly, you can follow the editor's instructions to test whether it functions in game. Alternatively, you can test by comparing the output with the following:

When the editor is initialized, type "Test" on six different lines with the following edits where applicable:
1. First 'Test' string has no modifications
2. Second 'Test' string is bold
3. Third 'Test' string is italicized
4. Fourth 'Test' string is both bold and italicized
5. Fifth 'Test' string has a different color from the default.
6. Sixth 'Test' string has a different size from the default.

Once you have inserted this into the editor, run the translator and see if the output contains the following commands (without the spaces between <> or ; as those are there to prevent the readme from registering those as actual commands:

1. &lt ;i&gt ;
2. &lt ;b&gt ;
3. &lt ;color=___&gt ; (as a hex code)
4. &lt ;size=___%&gt ;
5. < description >

Should it have all five of those present, then the editor is working properly.

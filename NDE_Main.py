# Main Editor: Takes user input and processes it for other modules.

# Initialize window for user
# Set window size
# Set window title

# Initialize tkinter text "widget"

# Initialize Scrollbar

# Establish Text Variables (Typograph, Size, Color) (So they can be referred to later especially by other modules) (lambda commands)

# Establish Text Format Commands (Applies NDE Typograph, NDE Size, and NDE Color, stores values for reference in other modules)

# Analyze User Input, determine if it has unsupported characters (Zalgo Text, Emojis, etc.)
# if unsupported characters are found, display error message and ask user to correct input.
# else, proceed with formatting.

# Apply Module Imports (NDE_Export, NDE_Color, NDE_Typograph, NDE_Size)
# Imports are to be applied in order of inside to outside):
# 1. Import NDE_Size
# 2. Import NDE_Typograph
# 3. Import NDE_Color
# 4. Import NDE_Export

# Display Output: 
# Add instructions for user as needed

import tkinter as tk
from tkinter import font, colorchooser, simpledialog, messagebox
import re

from NDE_Size import apply_size_tags
from NDE_Typograph import apply_typograph_tags
from NDE_Color import apply_color_tags
from NDE_Export import export_description

# Usage instructions for the user.
USAGE_TEXT = (
    "USAGE: To properly use the editor, follow these steps:\n"
    "1. Insert text, format it how you like.\n"
    "2. The editor is only intended to work with traditional text, avoid using emoji's or other kinds of odd text where possible.\n"
    "3. Press the translate button, and copy the output.\n"
    "4. Paste the output by going into the fleet you want to add the description to. This can be often found in (Drive game is in) > Program Files (x86) > Steam > steamapps > common > Nebulous > Saves > Fleets\n"
    "5. Test in game to ensure it works!\n"
    "Note: Buttons only work when you have something drag selected."
)

def is_traditional_text(s):
    # Returns True if all characters are "traditional" (basic Latin, common punctuation, etc.)
    return all(ord(c) < 128 for c in s)

class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Text Editor")
        self.geometry("950x600")

        # Layout frames
        main_frame = tk.Frame(self)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_frame = tk.Frame(self, width=300)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Toolbar
        toolbar = tk.Frame(main_frame)  # Create a frame to hold toolbar buttons, placed in the main_frame
        toolbar.pack(side=tk.TOP, fill=tk.X)  # Pack the toolbar at the top of main_frame, filling horizontally

        self.current_font_family = "Arial"  # Set the default font family for text formatting
        self.current_font_size = 12  # Set the default font size for text formatting
        self.current_fg_color = "#000000"  # Set the default foreground (text) color

        self.bold_btn = tk.Button(toolbar, text="Bold", command=self.toggle_bold)  # Create a button for bold formatting, calls toggle_bold when clicked
        self.bold_btn.pack(side=tk.LEFT, padx=2, pady=2)  # Pack the bold button to the left of the toolbar with padding
        self.italic_btn = tk.Button(toolbar, text="Italic", command=self.toggle_italic)  # Create a button for italic formatting, calls toggle_italic when clicked
        self.italic_btn.pack(side=tk.LEFT, padx=2, pady=2)  # Pack the italic button to the left of the toolbar with padding
        self.size_btn = tk.Button(toolbar, text="Font Size", command=self.change_font_size)  # Create a button to change font size, calls change_font_size when clicked
        self.size_btn.pack(side=tk.LEFT, padx=2, pady=2)  # Pack the font size button to the left of the toolbar with padding
        self.color_btn = tk.Button(toolbar, text="Text Color", command=self.change_text_color)  # Create a button to change text color, calls change_text_color when clicked
        self.color_btn.pack(side=tk.LEFT, padx=2, pady=2)  # Pack the color button to the left of the toolbar with padding

        # Translate button
        self.translate_btn = tk.Button(toolbar, text="Translate", command=self.translate_text)  # Create a button to translate/convert the text, calls translate_text when clicked
        self.translate_btn.pack(side=tk.LEFT, padx=10, pady=2)  # Pack the translate button to the left of the toolbar with extra horizontal padding

        # Main text widget
        self.text = tk.Text(main_frame, wrap="word", undo=True, font=(self.current_font_family, self.current_font_size))  # Create the main text editing widget with word wrap and undo enabled, using the default font and size
        self.text.pack(expand=1, fill="both")  # Pack the text widget to expand and fill available space in main_frame

        # Output label and output/copy frame
        output_label = tk.Label(main_frame, text="Translated Output:")  # Create a label for the translated output section
        output_label.pack()  # Pack the output label

        output_frame = tk.Frame(main_frame)  # Create a frame to hold the output text widget and copy button
        output_frame.pack(fill="x", padx=5, pady=(0,5))  # Pack the output frame horizontally with padding

        self.output = tk.Text(output_frame, height=8, wrap="word", state="disabled", bg="#f0f0f0")  # Create a disabled text widget for displaying the translated output
        self.output.pack(side=tk.LEFT, fill="both", expand=True)  # Pack the output widget to the left, filling available space

        self.copy_btn = tk.Button(output_frame, text="Copy Output", command=self.copy_output)  # Create a button to copy the output text to the clipboard
        self.copy_btn.pack(side=tk.RIGHT, padx=5, pady=5)  # Pack the copy button to the right with padding

        # Info panel
        info_label = tk.Label(info_frame, text="Information", font=("Arial", 14, "bold"))  # Create a label for the information panel
        info_label.pack(pady=(10,0))  # Pack the info label with top padding
        info_text = tk.Text(info_frame, wrap="word", height=20, width=40, bg="#e8e8e8", borderwidth=0)  # Create a text widget for usage instructions in the info panel
        info_text.insert("1.0", USAGE_TEXT)  # Insert the usage instructions into the info panel
        info_text.config(state="disabled")  # Set the info panel text widget to read-only
        info_text.pack(padx=10, pady=10, fill="both", expand=True)  # Pack the info panel text widget with padding and fill

        self.configure_tags()  # Call the method to configure text formatting tags

    def configure_tags(self):  # Define method to configure tags for bold, italic, color, and size
        self.text.tag_configure("bold", font=(self.current_font_family, self.current_font_size, "bold"))  # Configure the "bold" tag
        self.text.tag_configure("italic", font=(self.current_font_family, self.current_font_size, "italic"))  # Configure the "italic" tag
        self.text.tag_configure("bold_italic", font=(self.current_font_family, self.current_font_size, "bold", "italic"))  # Configure the "bold_italic" tag
        self.text.tag_configure("color", foreground=self.current_fg_color)  # Configure the "color" tag
        self.text.tag_configure("size", font=(self.current_font_family, self.current_font_size))  # Configure the "size" tag

    def toggle_bold(self):  # Define method to toggle bold formatting on selected text
        self.apply_style_tag("bold")  # Call apply_style_tag with "bold"

    def toggle_italic(self):  # Define method to toggle italic formatting on selected text
        self.apply_style_tag("italic")  # Call apply_style_tag with "italic"

    def change_font_size(self):  # Define method to change font size of selected text
        size = simpledialog.askinteger("Font Size", "Enter font size (in points):", minvalue=6, maxvalue=100)  # Prompt user for font size
        if size:  # If user entered a size
            try:
                start, end = self.text.index("sel.first"), self.text.index("sel.last")  # Get selection start and end, indexes are used for scanning and processing characters.
            except tk.TclError:
                return  # If no selection, do nothing
            idx = self.text.index(start)  # Start at selection start
            while self.text.compare(idx, "<", end):  # Loop through selection
                tags = self.text.tag_names(idx)  # Get tags at current index
                # Find bold/italic
                is_bold = False  # Track if bold is set
                is_italic = False  # Track if italic is set
                for tag in tags:
                    if "bold" in tag:
                        is_bold = True
                    if "italic" in tag:
                        is_italic = True
                # Remove all size/bold/italic tags at this index
                for tag in tags:
                    if tag.startswith("size_") or "bold" in tag or "italic" in tag:
                        self.text.tag_remove(tag, idx, f"{idx}+1c")
                # Build new tag name and font
                tag_name = f"size_{size}"
                font_tuple = [self.current_font_family, size] # Uses tuples mainly for immutability.
                if is_bold and is_italic: # Applies a bold italic tag if a text is both bold and italic
                    tag_name += "_bold_italic"
                    font_tuple += ["bold", "italic"]
                elif is_bold: # Otherwise applies only bold if bold.
                    tag_name += "_bold"
                    font_tuple += ["bold"]
                elif is_italic: # Otherwise applies only italic if italic.
                    tag_name += "_italic"
                    font_tuple += ["italic"]
                # Configure tag if needed
                if tag_name not in self.text.tag_names():
                    self.text.tag_configure(tag_name, font=tuple(font_tuple))
                # Add tag to this character
                self.text.tag_add(tag_name, idx, f"{idx}+1c")
                idx = self.text.index(f"{idx}+1c")  # Move to next character
        
    def change_text_color(self):  # Define method to change color of selected text
        color = colorchooser.askcolor(title="Choose text color", initialcolor=self.current_fg_color)  # Prompt user for color
        if color and color[1]:  # If user selected a color
            self.current_fg_color = color[1]  # Update current color
            tag_name = f"color_{self.current_fg_color.lstrip('#')}"  # Build tag name for color
            self.text.tag_configure(tag_name, foreground=self.current_fg_color)  # Configure color tag
            try:
                start, end = self.text.index("sel.first"), self.text.index("sel.last")  # Get selection start and end
            except tk.TclError:
                return  # If no selection, do nothing
            self.text.tag_add(tag_name, start, end)  # Add color tag to selection

    def toggle_bold(self):  # Define method to toggle bold formatting (duplicate for toolbar)
        self.apply_style_tag("bold")  # Call apply_style_tag with "bold"

    def toggle_italic(self):  # Define method to toggle italic formatting (duplicate for toolbar)
        self.apply_style_tag("italic")  # Call apply_style_tag with "italic"

    def copy_output(self):  # Define method to copy output text to clipboard
        self.clipboard_clear()  # Clear clipboard
        self.clipboard_append(self.output.get("1.0", "end-1c"))  # Copy output text to clipboard
        messagebox.showinfo("Copied", "Output copied to clipboard!")  # Show confirmation message

    def get_all_runs(self, text):  # Define method to get all formatting runs in the text
        # Build a list of (start, end, size, bold, italic, color)
        font_info = self.get_font_info(text)  # Get font size runs
        style_info = self.get_style_info(text)  # Get style (bold/italic) runs
        color_info = self.get_color_info(text)  # Get color runs

        # Collect all change points (This is what allows splitting the text into segments that have consistent formatting)
        change_points = set()  # Set to store all change points
        for start, end, *_ in font_info: # Collect start and end points of font size runs
            change_points.add(start) 
            change_points.add(end)
        for start, end, *_ in style_info: # Collect start and end points of style runs
            change_points.add(start)
            change_points.add(end)
        for start, end, *_ in color_info: # Collect start and end points of color runs
            change_points.add(start)
            change_points.add(end)
        change_points = sorted([pt for pt in change_points if pt < len(text)])  # Sort and filter change points

        # Build runs
        runs = []  # List to store runs
        for i in range(len(change_points) - 1):
            s, e = change_points[i], change_points[i+1]
            # Find formatting for this run
            size = next(sz for st, en, sz in font_info if st <= s < en)
            bold, italic = next((b, i) for st, en, b, i in style_info if st <= s < en)
            color = next(c for st, en, c in color_info if st <= s < en)
            runs.append((s, e, size, bold, italic, color))
        # Handle last run if needed
        if change_points:
            s = change_points[-1]
            if s < len(text):
                size = next(sz for st, en, sz in font_info if st <= s < en)
                bold, italic = next((b, i) for st, en, b, i in style_info if st <= s < en)
                color = next(c for st, en, c in color_info if st <= s < en)
                runs.append((s, len(text), size, bold, italic, color))
        return runs

    def translate_text(self):  # Define method to translate text and apply tags
        raw_text = self.text.get("1.0", "end-1c")  # Get all text from editor
        if not raw_text.strip():
            self.display_output("")  # If empty, clear output
            return

        runs = self.get_all_runs(raw_text)  # Get formatting runs
        default_size = 12  # or self.current_font_size if you want

        result = ""  # Initialize result string
        for start, end, size, bold, italic, color in runs:
            segment = raw_text[start:end] # Extract the segment of text for this run
            if not is_traditional_text(segment): # Check if segment is traditional text
                result += segment
                continue
            percent = int(round(size / default_size * 100))
            seg = segment
            # Apply tags in order: size, bold, italic, color
            if percent != 100:
                seg = f"&lt;size={percent}%&gt;{seg}&lt;/size&gt;" # Applies size tags, saving on formatting if size should be interpreted as default.
            if bold and italic:
                seg = f"&lt;b&gt;&lt;i&gt;{seg}&lt;/i&gt;&lt;/b&gt;" # Applies bold and italic.
            elif bold:
                seg = f"&lt;b&gt;{seg}&lt;/b&gt;" # Applies bold only.
            elif italic:
                seg = f"&lt;i&gt;{seg}&lt;/i&gt;" # Applies italic only.
            if color and color.lower() != "#000000": 
                seg = f"&lt;color={color}&gt;{seg}&lt;/color&gt;" # Applies color tags, saving on formatting if color should be interpreted as default.
            result += seg

        final_output = export_description(result)  # Wrap result in export tags
        self.display_output(final_output)  # Display output

    def display_output(self, text):  # Define method to display output in output widget
        self.output.config(state="normal")  # Enable output widget
        self.output.delete("1.0", "end")  # Clear output widget
        self.output.insert("1.0", text)  # Insert new output
        self.output.config(state="disabled")  # Disable output widget

    def _tag_font_style(self, tag):  # Helper method to get font style tuple from tag
        if tag == "bold":
            return ("bold",)
        elif tag == "italic":
            return ("italic",)
        elif tag == "bold_italic":
            return ("bold", "italic")
        else:
            return tuple()

    def apply_style_tag(self, style):  # Define method to apply/toggle style tag (bold/italic) to selection
        try:
            start, end = self.text.index("sel.first"), self.text.index("sel.last")
        except tk.TclError:
            return

        idx = self.text.index(start)
        while self.text.compare(idx, "<", end):
            tags = self.text.tag_names(idx)
            # Find size from tags, default to current font size
            size = self.current_font_size
            for tag in tags:
                m = re.match(r"size_(\d+)", tag)
                if m:
                    size = int(m.group(1))
                    break
            # Find bold/italic
            is_bold = False
            is_italic = False
            for tag in tags:
                if "bold" in tag:
                    is_bold = True
                if "italic" in tag:
                    is_italic = True
            # Toggle as needed
            if style == "bold":
                is_bold = not is_bold
            elif style == "italic":
                is_italic = not is_italic
            # Remove all size/bold/italic tags at this index
            for tag in tags:  # Iterate through all tags at the current index
                if tag.startswith("size_") or "bold" in tag or "italic" in tag:  # If tag is size, bold, or italic
                    self.text.tag_remove(tag, idx, f"{idx}+1c")  # Remove the tag from the current character
            # Build new tag name and font
            tag_name = f"size_{size}"  # Start building the tag name with the size
            font_tuple = [self.current_font_family, size]
            if is_bold and is_italic:
                tag_name += "_bold_italic"
                font_tuple += ["bold", "italic"]
            elif is_bold:
                tag_name += "_bold"
                font_tuple += ["bold"]
            elif is_italic:
                tag_name += "_italic"
                font_tuple += ["italic"]
            # Configure tag if needed
            if tag_name not in self.text.tag_names():
                self.text.tag_configure(tag_name, font=tuple(font_tuple))
            # Add tag to this character
            self.text.tag_add(tag_name, idx, f"{idx}+1c")
            idx = self.text.index(f"{idx}+1c")

    # --- Helper methods to extract tag info from the Text widget ---

    def get_font_info(self, text):  # Helper to get font size runs
        result = []
        idx = 0
        start = 0
        last_size = None # Sets default parameters
        text_length = len(text)
        while idx < text_length:
            tag_indices = self.text.tag_names(f"1.0+{idx}c")
            size = self.current_font_size
            for tag in tag_indices:
                m = re.match(r"size_(\d+)", tag) # Figures out the size without it having to be specifically defined by a number.
                if m:
                    size = int(m.group(1))
                    break
            if last_size is None:
                last_size = size
            if size != last_size: # Determines whether the previous parameter is the same as the current one on the character being checked.
                result.append((start, idx, last_size)) # Appends the start index, end index, and size of the previous run to ensure the translation output is accomodated.
                start = idx
                last_size = size
            idx += 1
        if start < text_length:
            result.append((start, text_length, last_size))
        return result

    def get_style_info(self, text):  # Helper to get style (bold/italic) runs
        result = []
        idx = 0
        start = 0
        last_bold = None
        last_italic = None
        while idx < len(text):
            tag_indices = self.text.tag_names(f"1.0+{idx}c")
            is_bold = any("bold" in tag for tag in tag_indices)
            is_italic = any("italic" in tag for tag in tag_indices)
            if last_bold is None:
                last_bold = is_bold
                last_italic = is_italic
            if (is_bold, is_italic) != (last_bold, last_italic):
                result.append((start, idx, last_bold, last_italic))
                start = idx
                last_bold = is_bold
                last_italic = is_italic
            idx += 1
        if start < len(text):
            result.append((start, len(text), last_bold, last_italic))
        return result

    def get_color_info(self, text):  # Helper to get color runs
        result = []
        idx = 0
        start = 0
        last_color = None
        text_length = len(text)
        while idx < text_length:
            tag_indices = self.text.tag_names(f"1.0+{idx}c")
            color = None
            # Look for a tag like 'color_#RRGGBB'
            for tag in tag_indices:
                m = re.match(r"color_([0-9a-fA-F]{6})", tag)
                if m:
                    color = f"#{m.group(1)}"
                    break
            if color is None:
                color = "#000000"  # Default color if no tag (This is only needed for the editor, specifically for the user to see what they are typing. Translation side doesn't need this.)
            if last_color is None:
                last_color = color
            if color != last_color:
                result.append((start, idx, last_color))
                start = idx
                last_color = color
            idx += 1
        if start < text_length:
            result.append((start, text_length, last_color))
        return result

if __name__ == "__main__":  # If this script is run directly
    app = TextEditor()  # Create the TextEditor application
    app.mainloop()  # Start the Tkinter event loop

    #Daniel's Comments:

    #So all of this was actually generated by AI, although we did need it to go back and make some changes to the code to get it to work properly.
    #For the original generation of the code, we used the following prompt:
    
    #"So, we need to make a text editor in Python using Tkinter. It should have a toolbar with buttons for bold, italic, font size, and text color. Use the following below as a guideline:"
    
    #1. user can input and see text
    #2. user can apply bold and italics to their input and see that in the editor
    #3. user can change the text size (in points) of their input and see that in the editor
    #4. user can change the text color (ideally as a hex code, we may need an additional library for that) of their input and see that in the editor


    #Once CoPilot generated the code, we ran it and found that it did not work properly. We then went back and used this prompt to try and have it fix the issues in the code:

    #"So there ar a couple issues that we need to fix in your code. First of, we need to make it so that way you can apply bold and italic at the same time. They also need to work if you change the font size as well."


    #After that, CoPilot fixed those isues that we were having with the code. We than ran it again and found that it still did not work properly with one other thing, so we used this prompt as well to attempt to fix it:

    #"Okay that was good but we still have one issue. We also need the text size to actually apply if the text already has bold or italics applied to it."

    #It then made the final changes to the code and ran properly!


    #Nathaniel's Comments:

    #For Modules, I used the following prompt:

    #"Allow me to explain the overall needs of this editor. NDE Main is the editor itself that needs to apply all of the other NDE files given as context to get an output. The NDE files aside from the main each have their own job they need to do as described: NDE size should first identify characters that have a font size different than font size 12. From there, it needs to calculate the difference in font size as a percentage by performing arithmetic. It should be able to distinguish the text by strings of characters that can be grouped if directly adjacent to another character that is the exact same font size as itself. This method of string sorting goes for all the other NDE modules aside from the main, though for them it will be respective to their specific function, like determining color, whether it is italics or bold, etc. In particular, the NDE Size needs to be able to differentiate strings of text based on size and apply it in the form of this command: "<size=(insert percentage as integer)%>'String Text'</size>", so that the main editor can apply it to text that it sees.
    #Should you be able to modify other NDE files used for context as well as this one, the other NDE files inevitably need a similar conversion, as described below:
    #NDE color identies grouped characters of the same color, and formats it in the form of a command "<color=#Hex Code>'String Text'</color&gt".
    #NDE Typograph takes specifically two different functions. It groups by what is italicized and what is bold, grouped independently of one another just like the rest of the modules. It then takes the italics and formats a command around it: "<i>'String Text'</i>". Bold has a similar format: "<b>'String Text'</b&gt"
    #NDE Export should be applied last (the order of application doesn't necessarily matter in the main editor but we can stick with Size being applied first, then italics/bold, then color and finally NDE export). NDE Export simply takes the entirety of the Main's combined output of all the other modules, treats it as a singular string and applies <description> and </description> around it, ideally on a line before and after the main text itself. Can you modify the code of all corresponding files to fit those specifications?"

    #I then used a second prompt to modify the original Main to accomodate the functions and gather the necessary data to construct the editor:

    #Precisely, now the main editor needs to be able to process the information and apply the tags to get the final output, though there are a few caveats that are ideal to implement:
    #A. The main editor should ideally apply this output only when the user presses a button named "Translate", and the output should be placed separately in the window, for example perhaps underneath the main text editing section there is another which displays solely the output.
    #B. The other section which contains the translated text should have a copy button that allows the user to not have to Ctrl+C the text.
    #C. I want the main editor itself to have a information panel (perhaps a section much like what is described in point A.) to the right of the main editor when the window is open. I want it to display the following text:
    #"USAGE: To properly use the editor, follow these steps:
    #1. Insert text, format it how you like.
    #2. The editor is only intended to work with traditional text, avoid using emoji's or other kinds of odd text where possible.
    #3. Press the translate button, and copy the output.
    #4. Paste the output by going into the fleet you want to add the description to. This can be often found in (Drive game is in) > Program Files (x86) > Steam > steamapps > common > Nebulous > Saves > Fleets
    #5. Test in game to ensure it works!"
    #D. Should the user enter something irregular like an emoji, something that is not traditional text, have the code avoid applying any translations to it for the output.

    #The code ran into some issues while running. Any attempts made to fix errors are listed below:
   
    #The terminal suggests that no module called NDE_Size exists, I suspect it may not recognize the files either due to incorrect naming or a potentially missed setup step. Can you find any more additional information on the issue and potentially resolve it? I believe this issue might apply to all the other tags but I am not certain.
    
    # Error resolved: Modules cannot contain spaces, renamed files to avoid issue.

    #The editor runs but there are several issues that need to be addressed:
    #1. The font size changes the actual editor's text size too, so the information panel disappears and so does the translated output panel. They should stay visible in the screen relative to its size, not scale with the rest of the text. Additionally, the font size should only change highlighted characters (characters that the user drags over and selects) as opposed to the entire text in the window.
    #2. The output needs to match the very specific format I was mentioning. If it replaces &lt; and &gt;with their physical < > representations it will not work as intended. I need the commands to stay the way they normally are.
    #3. There may need to be a mechanism to lock what the actual input is. I believe the code as it stands is applying tags to the string as well as the tags surrounding the string that were previously implemented. The commands should only format themselves around the user's input, preferably in a way that doesn't interfere with the formatting of other commands attempting to simultaneously modify the user's input.

    #AI provided revised code to fix font size issues. I manually edited all modules to format with &lt; and &gt;instead of < and >.

    #For the third segment, the solution I am looking for is that it still applies all the tags, that is not the problem. The issue is, for example, if I have a string "Text", instead of formatting as (this is just a basic example simplified) <color><i><b><size>'Text'</color></i></b></size> it instead formats as <color><color><i><i><b><b><size>'Text'</size>... I need it to apply all the tags neatly, not chaotically to where it likely does not work. There are also two other caveats I would like to address:
    #1. The copy button for the output section is missing. I am not sure where it is.
    #2. For the size, the terminal is suggesting the size tags are not defined in the text widget. This means I cannot format size at all. It would be ideal for size commands to work again.

    #Managed to fix the size issue but it took a lot of rewriting. Had to fix miscellaneous syntax issues.
    #Copy button fixed, it was masked behind one of the other buttons. AI helped me move it to a different location.
    #Color tag apparently applied broadly to the entire segment.
    #Huge formatting issues with the translation, took a lot of prompts to sort that out. Had to swap to dynamic tags to make it work properly.
    #NOTE: This version includes some data saving methods but does not have peak efficiency yet. It applies all the tags properly based on what adjacent characters have *all* the same properties, but if even one property is not the same it splits them and separately applies all tags around them. It is better than it always being applied to each individual character, but may not be ideal if someone wants to make some really whacky designs while still maintaining maximum data compression.
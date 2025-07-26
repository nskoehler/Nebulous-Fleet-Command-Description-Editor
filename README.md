# Nebulous-Fleet-Command-Description-Editor
This is the official repository for the Nebulous: Fleet Command Text Editor

The Nebulous Fleet Command Description Editor is a Text Editor designed for use with the game Nebulous: Fleet Command. It allows you to input text with different colors, sizes and typographs, exporting them in a manner that can simply be copy pasted into the .fleet file of one's choice between the <FactionKey> and <SortOverrideOrder> tags at the start of file (usually at lines 6-7 respectively).

You need python to run the files, and to run the editor properly ensure you initialize from NDE_Main.py specifically.

To test whether or not the editor functions properly, you can follow the editor's instructions to test whether it functions in game. Alternatively, you can test by comparing the output with the following:

When the editor is initialized, type "Test" on six different lines with the following edits where applicable:
1. First 'Test' string has no modifications
2. Second 'Test' string is bold
3. Third 'Test' string is italicized
4. Fourth 'Test' string is both bold and italicized
5. Fifth 'Test' string has a different color from the default.
6. Sixth 'Test' string has a different size from the default.

Once you have inserted this into the editor, run the translator and see if the output contains the following commands:

1. &lt;i&gt;
2. &lt;b&gt;
3. &lt;color=___&gt; (as a hex code)
4. &lt;size=___%&gt;
5. <description>

Should it have all five of those present, then the editor is working properly.

from services.window import TextEditorWindow

text_editor = TextEditorWindow()

text_editor.text_box.pack(expand=1, fill="both")
text_editor.window.protocol("WM_DELETE_WINDOW", text_editor.on_closing)
text_editor.window.bind("<Key>", text_editor.key_pressed)
text_editor.window.mainloop()


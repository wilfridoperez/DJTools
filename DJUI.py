import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("DJ Mixer")
root.configure(bg="#23252a")

# Top bar
top_frame = tk.Frame(root, bg="#23252a")
top_frame.pack(fill="x", pady=10)

tk.Button(top_frame, text="+", bg="#333", fg="white", font=("Arial", 16), width=2, relief="flat").pack(side="left", padx=10)
tk.Label(top_frame, text="DJ FREE", bg="#23252a", fg="#888", font=("Arial", 18, "bold")).pack(side="left", expand=True)
tk.Label(top_frame, text="DJ FREE", bg="#23252a", fg="#888", font=("Arial", 18, "bold")).pack(side="right", expand=True)
tk.Button(top_frame, text="+", bg="#333", fg="white", font=("Arial", 16), width=2, relief="flat").pack(side="right", padx=10)

# Decks frame
decks_frame = tk.Frame(root, bg="#23252a")
decks_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Left Deck
left_deck = tk.Frame(decks_frame, bg="#23252a")
left_deck.pack(side="left", expand=True, fill="both", padx=10)

tempo_a = tk.Scale(left_deck, from_=-100, to=100, orient="vertical", length=200, bg="#23252a", fg="white", troughcolor="#444", highlightthickness=0)
tempo_a.set(0)
tempo_a.pack(side="left", padx=10)

canvas_a = tk.Canvas(left_deck, width=180, height=180, bg="#23252a", highlightthickness=0)
canvas_a.pack()
# Draw orange platter
canvas_a.create_oval(10, 10, 170, 170, fill="#ff9900", outline="#ff9900")
canvas_a.create_polygon(90, 50, 120, 90, 90, 130, fill="white")  # Play triangle

# Buttons under deck A
btn_frame_a = tk.Frame(left_deck, bg="#23252a")
btn_frame_a.pack(pady=10)
tk.Button(btn_frame_a, text="CUE", width=6, bg="#444", fg="white").pack(side="left", padx=5)
tk.Button(btn_frame_a, text="▶", width=6, bg="#444", fg="white").pack(side="left", padx=5)
tk.Button(btn_frame_a, text="SYNC", width=6, bg="#444", fg="white").pack(side="left", padx=5)

# Right Deck
right_deck = tk.Frame(decks_frame, bg="#23252a")
right_deck.pack(side="right", expand=True, fill="both", padx=10)

tempo_b = tk.Scale(right_deck, from_=-100, to=100, orient="vertical", length=200, bg="#23252a", fg="white", troughcolor="#444", highlightthickness=0)
tempo_b.set(0)
tempo_b.pack(side="right", padx=10)

canvas_b = tk.Canvas(right_deck, width=180, height=180, bg="#23252a", highlightthickness=0)
canvas_b.pack()
# Draw blue platter
canvas_b.create_oval(10, 10, 170, 170, fill="#0099ff", outline="#0099ff")
canvas_b.create_polygon(90, 50, 120, 90, 90, 130, fill="white")  # Play triangle

# Buttons under deck B
btn_frame_b = tk.Frame(right_deck, bg="#23252a")
btn_frame_b.pack(pady=10)
tk.Button(btn_frame_b, text="SYNC", width=6, bg="#444", fg="white").pack(side="left", padx=5)
tk.Button(btn_frame_b, text="CUE", width=6, bg="#444", fg="white").pack(side="left", padx=5)
tk.Button(btn_frame_b, text="▶", width=6, bg="#444", fg="white").pack(side="left", padx=5)

# Crossfader
crossfader_frame = tk.Frame(root, bg="#23252a")
crossfader_frame.pack(pady=10)
tk.Scale(crossfader_frame, from_=0, to=1, orient="horizontal", length=300, resolution=0.01, bg="#23252a", fg="white", troughcolor="#444", highlightthickness=0).pack()

root.mainloop()
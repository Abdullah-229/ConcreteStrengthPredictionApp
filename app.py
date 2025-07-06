import tkinter as tk
from tkinter import messagebox
import joblib
import numpy as np
import database
import threading

# --- Database Setup ---
db_conn = database.create_connection()
if db_conn:
    database.create_table(db_conn)

# Load trained XGBoost models
model_mean = joblib.load("models/xgboost_model_strength.joblib")   # Mean prediction model
model_q10 = joblib.load("./models/xgb_quantile_model_10.joblib")     # 10th percentile model
model_q90 = joblib.load("./models/xgb_quantile_model_90.joblib")     # 90th percentile model

# Feature names and units
features = [
    ("Cement (kg/m³)", "cement"),
    ("Blast Furnace Slag (kg/m³)", "slag"),
    ("Fly Ash (kg/m³)", "flyash"),
    ("Water (kg/m³)", "water"),
    ("Superplasticizer (kg/m³)", "superplasticizer"),
    ("Coarse Aggregate (kg/m³)", "coarseagg"),
    ("Fine Aggregate (kg/m³)", "fineagg"),
    ("Age (days)", "age"),
]

# --- Light Green Theme ---
BG_GRADIENT_TOP = "#f0f9f0"      # Light green-white
BG_GRADIENT_BOTTOM = "#e0f2e0"   # Soft green
ACCENT1 = "#4caf50"              # Vibrant green
ACCENT2 = "#81c784"              # Lighter green
ACCENT3 = "#388e3c"              # Darker green for results text
BUTTON_BG = "#90ee90"              # Light green
BUTTON_HOVER = "#66bb6a"
CLEAR_BUTTON_BG = "#e0e0e0"
CLEAR_BUTTON_HOVER = "#d0d0d0"
BUTTON_TEXT = "#000000"           # Black for button text
ENTRY_BG = "#ffffff"             # White
ENTRY_BORDER = "#cccccc"
RESULT_BG = "#f0f9f0"             # Light green-white
RESULT_BORDER = ACCENT1           # Accent border for result box
CARD_BG = "#ffffff"              # White
FOOTER_BG = "#f0f9f0"
TEXT_COLOR = "#333333"            # Dark gray for all text
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 20, "bold")
RESULT_FONT = ("Segoe UI", 13, "bold")

# --- Main Window ---
root = tk.Tk()
root.title("Concrete Strength Predictor")
root.geometry("540x700")
root.minsize(420, 600)
root.configure(bg=BG_GRADIENT_TOP)

# --- Gradient-like background using color blocks ---
gradient_top = tk.Frame(root, bg=BG_GRADIENT_TOP, height=120)
gradient_top.pack(fill="x", side="top")
gradient_bottom = tk.Frame(root, bg=BG_GRADIENT_BOTTOM)
gradient_bottom.pack(fill="both", expand=True)

# --- Title ---
title = tk.Label(gradient_top, text="Concrete Strength Predictor", font=TITLE_FONT, bg=BG_GRADIENT_TOP, fg=ACCENT1)
title.pack(pady=(30, 10))

# --- Card-like form frame ---
entries = {}
form_frame = tk.Frame(gradient_bottom, bg=BG_GRADIENT_BOTTOM, bd=0, highlightbackground="#334155", highlightthickness=1)
form_frame.place(relx=0.5, rely=0.05, anchor="n", relwidth=0.92)
form_frame.pack_propagate(False)
form_frame.columnconfigure(1, weight=1)

for i, (label_text, feature_key) in enumerate(features):
    label = tk.Label(form_frame, text=label_text, font=FONT, bg=CARD_BG, fg=TEXT_COLOR)
    label.grid(row=i, column=0, sticky="w", pady=7, padx=(0, 10))
    entry_frame = tk.Frame(form_frame, bg=ENTRY_BORDER, bd=0)
    entry_frame.grid(row=i, column=1, sticky="ew", pady=7)
    entry = tk.Entry(entry_frame, font=FONT, width=18, bg=ENTRY_BG, relief="flat", highlightthickness=0, bd=0, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
    entry.pack(padx=1, pady=1, fill="x")
    entry.insert(0, "0")
    entries[feature_key] = entry
form_frame.grid_columnconfigure(1, weight=1)

# --- Button Frame ---
button_frame = tk.Frame(gradient_bottom, bg=BG_GRADIENT_BOTTOM)
button_frame.place(relx=0.5, rely=0.6, anchor="n", relwidth=0.92)

# --- Result area ---
result_frame = tk.Frame(gradient_bottom, bg=RESULT_BG, bd=0, highlightbackground=RESULT_BORDER, highlightthickness=2)
result_frame.place(relx=0.5, rely=0.7, anchor="n", relwidth=0.92)
result_label = tk.Label(result_frame, text="", font=RESULT_FONT, bg=RESULT_BG, fg=TEXT_COLOR, wraplength=400, justify="left")
result_label.pack(padx=10, pady=15, fill="x")

def clear_entries():
    for entry in entries.values():
        entry.delete(0, tk.END)
        entry.insert(0, "0")
    result_label.config(text="")

# --- Buttons with hover effect ---
def on_enter_submit(e):
    submit_btn.config(bg=BUTTON_HOVER)
def on_leave_submit(e):
    submit_btn.config(bg=BUTTON_BG)

def on_enter_clear(e):
    clear_btn.config(bg=CLEAR_BUTTON_HOVER)
def on_leave_clear(e):
    clear_btn.config(bg=CLEAR_BUTTON_BG)

submit_btn = tk.Button(
    button_frame,
    text="Submit",
    command=lambda: predict_strength(),
    font=("Segoe UI", 14, "bold"),
    bg=BUTTON_BG,
    fg=BUTTON_TEXT,
    activebackground=BUTTON_HOVER,
    activeforeground=BUTTON_TEXT,
    bd=0,
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    highlightthickness=0,
    borderwidth=0,
)
submit_btn.pack(side="left", expand=True, padx=10, pady=10)
submit_btn.bind("<Enter>", on_enter_submit)
submit_btn.bind("<Leave>", on_leave_submit)

clear_btn = tk.Button(
    button_frame,
    text="Clear",
    command=clear_entries,
    font=("Segoe UI", 14, "bold"),
    bg=CLEAR_BUTTON_BG,
    fg=BUTTON_TEXT,
    activebackground=CLEAR_BUTTON_HOVER,
    activeforeground=BUTTON_TEXT,
    bd=0,
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    highlightthickness=0,
    borderwidth=0,
)
clear_btn.pack(side="right", expand=True, padx=10, pady=10)
clear_btn.bind("<Enter>", on_enter_clear)
clear_btn.bind("<Leave>", on_leave_clear)

# --- Loading animation ---
loading_label = tk.Label(result_frame, text="", font=("Segoe UI", 12), bg=RESULT_BG, fg=ACCENT2)
loading_label.pack(pady=(0, 10))

def animate_loading():
    dots = [".", "..", "...", "...."]
    current = 0
    
    def update():
        nonlocal current
        loading_label.config(text=f"Predicting{dots[current]}")
        current = (current + 1) % len(dots)
        if loading_label.winfo_ismapped():
            root.after(500, update)
    
    update()

# --- Prediction logic with threading ---
import knowledge_base

# --- Prediction logic ---
def predict_strength():
    try:
        input_values = {key: float(entries[key].get()) for key in entries}
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields!")
        return

    warnings = knowledge_base.check_inputs(input_values)
    if warnings:
        messagebox.showwarning("Input Warning", "\n".join(warnings))
        result_label.config(text=(
            f"🔹 Predicted Mean Strength: 0.00 MPa\n\n"
            f"🔹 80% Probability Strength Range:\n"
            f"   ➔ Lower Bound (10th percentile): 0.00 MPa\n"
            f"   ➔ Upper Bound (90th percentile): 0.00 MPa"
        ), fg=ACCENT3)
        return

    # Disable button during prediction
    submit_btn.config(state=tk.DISABLED, bg="#6a737d")
    result_label.config(text="")
    loading_label.pack()
    animate_loading()

    def run_prediction():
        try:
            values_for_prediction = [input_values[feature[1]] for feature in features]
            X_input = np.array(values_for_prediction).reshape(1, -1);

            mean_strength = model_mean.predict(X_input)[0]
            q10_strength = model_q10.predict(X_input)[0]
            q90_strength = model_q90.predict(X_input)[0]

            result_text = (
                f"🔹 Predicted Mean Strength: {mean_strength:.2f} MPa\n\n"
                f"🔹 80% Probability Strength Range:\n"
                f"   ➔ Lower Bound (10th percentile): {q10_strength:.2f} MPa\n"
                f"   ➔ Upper Bound (90th percentile): {q90_strength:.2f} MPa"
            )
            result_label.config(text=result_text, fg=ACCENT3)

            if db_conn:
                prediction_data = tuple(values_for_prediction) + (mean_strength, q10_strength, q90_strength)
                database.insert_prediction(db_conn, prediction_data)

        except Exception as e:
            messagebox.showerror("Prediction Error", f"An unexpected error occurred: {e}")
            result_label.config(text="", fg=ACCENT3)
        finally:
            loading_label.pack_forget()
            submit_btn.config(state=tk.NORMAL, bg=BUTTON_BG)

    threading.Thread(target=run_prediction).start()

# --- Footer accent ---
footer = tk.Frame(root, bg=FOOTER_BG, height=30)
footer.pack(side="bottom", fill="x")
tk.Label(footer, text="© 2025 Concrete AI", bg=FOOTER_BG, fg="#94a3b8", font=("Segoe UI", 10)).pack(pady=5)

# --- Make form responsive ---
def on_resize(event):
    form_frame.place_configure(relwidth=0.92)
    button_frame.place_configure(relwidth=0.92)
    result_frame.place_configure(relwidth=0.92)
    result_label.config(wraplength=form_frame.winfo_width()-60)
root.bind('<Configure>', on_resize)

root.mainloop()

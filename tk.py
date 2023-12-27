import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from main import create_supabase_client, search_videos, SUPABASE_URL, SUPABASE_KEY

# Create a Supabase client
supabase_client = create_supabase_client(SUPABASE_URL, SUPABASE_KEY)

# Function to update the count of search results
def update_result_count(event):
    search_term = search_var.get()
    filtered_videos = search_videos(search_term, supabase_client)
    result_count_var.set(f"{len(filtered_videos)} results")

# Function to display search results
def display_search_results(event):
    search_term = search_var.get()
    filtered_videos = search_videos(search_term, supabase_client)
    # Clear previous results in the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    # Display new results in the scrollable frame
    for _, row in filtered_videos.iterrows():
        video_frame = ttk.Frame(scrollable_frame)
        video_frame.pack(fill='x', expand=True)
        # Construct and display thumbnail using videoID
        video_id = row['video_id']
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/default.jpg"
        response = requests.get(thumbnail_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        img_label = ttk.Label(video_frame, image=img)
        img_label.image = img  # Keep a reference
        img_label.pack(side='left')
        # Display title and creator
        ttk.Label(video_frame, text=row['video_name']).pack()
        ttk.Label(video_frame, text=row['creator']).pack()
        # Display link (as a label for simplicity)
        link_label = ttk.Label(video_frame, text=f"https://www.youtube.com/watch?v={video_id}", foreground="blue", cursor="hand2")
        link_label.pack()
        # Bind opening URL to label click
        link_label.bind("<Button-1>", lambda e, url=f"https://www.youtube.com/watch?v={video_id}": open_url(url))


# Open URL in web browser
def open_url(url):
    import webbrowser
    webbrowser.open(url)

# Main window setup
root = tk.Tk()
root.title("Video Search")

# Search entry setup
search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var)
search_entry.pack(fill='x', expand=True)
search_entry.bind('<Return>', display_search_results)

# Result count label setup
result_count_var = tk.StringVar()
result_count_label = ttk.Label(root, textvariable=result_count_var)
result_count_label.pack()

# Scrollable area setup
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Configure canvas and scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()

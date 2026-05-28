"""
Mental Awareness Companion
A supportive mental wellness chatbot built with Tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import random
from datetime import datetime


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def current_time():
    """Return formatted current timestamp."""
    return datetime.now().strftime("%H:%M")


def save_to_file(content):
    """Save chat history to a text file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Saved", "Chat history exported successfully!")


# ============================================================
# CHATBOT LOGIC CLASS
# ============================================================

class MentalHealthChatbot:
    """Rule-based chatbot logic."""

    def __init__(self):

        # Emotional keyword responses
        self.responses = {
            "stress": [
                "It sounds like you're under pressure. Try taking a few deep breaths and focusing on one task at a time.",
                "Stress can feel overwhelming. A short walk or hydration break may help reset your mind."
            ],

            "anxiety": [
                "I'm sorry you're feeling anxious. Try grounding yourself by naming 5 things you can see around you.",
                "Slow breathing exercises may help calm anxious thoughts."
            ],

            "sadness": [
                "I'm here with you. Sometimes journaling your thoughts can help process sadness.",
                "It's okay to have difficult days. Talking to someone you trust may help."
            ],

            "loneliness": [
                "Loneliness can be hard. Reaching out to a trusted friend or family member may help.",
                "You deserve connection and support. Even small conversations matter."
            ],

            "anger": [
                "Taking a pause before reacting can help during moments of anger.",
                "Try stepping away for a moment and focusing on your breathing."
            ],

            "motivation": [
                "Small steps still count as progress. You don't have to do everything at once.",
                "Consistency is more important than perfection."
            ],

            "happiness": [
                "That's wonderful to hear! Celebrate the small wins in your life.",
                "Happiness grows when we appreciate positive moments."
            ],

            "burnout": [
                "Burnout is a sign that your mind and body may need rest.",
                "Try prioritizing sleep, hydration, and taking breaks."
            ]
        }

        # Crisis phrases
        self.crisis_phrases = [
            "i want to give up",
            "i feel hopeless",
            "i hate my life",
            "i want to disappear",
            "suicide",
            "self harm"
        ]

        # Motivational quotes
        self.quotes = [
            "You are stronger than you think.",
            "Small progress is still progress.",
            "Your feelings are valid.",
            "Rest is productive too.",
            "Healing takes time, and that's okay.",
            "One step at a time is enough."
        ]

    def detect_emotion(self, text):
        """Detect emotional keywords."""
        text = text.lower()

        for emotion in self.responses:
            if emotion in text:
                return emotion

        return None

    def detect_crisis(self, text):
        """Detect crisis-related phrases."""
        text = text.lower()

        for phrase in self.crisis_phrases:
            if phrase in text:
                return True

        return False

    def get_response(self, user_text):
        """Generate chatbot response."""

        # Crisis detection
        if self.detect_crisis(user_text):
            return (
                "I'm really sorry you're feeling this way. "
                "You matter, and you deserve support.\n\n"
                "Please consider reaching out to a trusted person or a mental health professional.\n"
                "If you're in immediate danger, contact local emergency services or a crisis hotline.\n\n"
                "You do not have to face this alone."
            )

        # Emotion detection
        emotion = self.detect_emotion(user_text)

        if emotion:
            response = random.choice(self.responses[emotion])

            # Occasionally add a quote
            if random.random() > 0.5:
                response += f"\n\n💡 Quote: \"{random.choice(self.quotes)}\""

            return response

        # Default responses
        default_responses = [
            "I'm here to listen. Tell me more about how you're feeling.",
            "Your thoughts and feelings matter.",
            "Taking care of your mental wellness is important.",
            "Remember to be kind to yourself today."
        ]

        return random.choice(default_responses)


# ============================================================
# MAIN APPLICATION CLASS
# ============================================================

class MentalAwarenessApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Mental Awareness Companion")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)

        # Chatbot instance
        self.bot = MentalHealthChatbot()

        # Theme mode
        self.dark_mode = False

        # Timer variables
        self.timer_running = False
        self.timer_seconds = 60

        # Colors
        self.light_theme = {
            "bg": "#EAF4F4",
            "chat_bg": "#FFFFFF",
            "user": "#D6EAF8",
            "bot": "#E8F8F5",
            "text": "#222222"
        }

        self.dark_theme = {
            "bg": "#1E1E2E",
            "chat_bg": "#2B2B3C",
            "user": "#3A506B",
            "bot": "#4B6584",
            "text": "#FFFFFF"
        }

        self.theme = self.light_theme

        # Configure root background
        self.root.configure(bg=self.theme["bg"])

        # Build UI
        self.create_menu()
        self.create_widgets()
        self.apply_theme()

        # Welcome message
        self.display_bot_message(
            "Hello 👋\n\n"
            "Welcome to Mental Awareness Companion.\n"
            "I'm here to support emotional awareness, mindfulness, "
            "and positive self-reflection.\n\n"
            "How are you feeling today?"
        )

        # Keyboard shortcuts
        self.root.bind("<Return>", lambda event: self.send_message())
        self.root.bind("<Control-s>", lambda event: self.export_chat())
        self.root.bind("<Control-l>", lambda event: self.clear_chat())

    # ========================================================
    # UI CREATION
    # ========================================================

    def create_menu(self):
        """Create application menu."""

        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Export Chat", command=self.export_chat)
        file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Toggle Dark/Light Mode",
                              command=self.toggle_theme)

        menu_bar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=menu_bar)

    def create_widgets(self):
        """Create all GUI components."""

        # ==========================
        # TOP FRAME
        # ==========================

        top_frame = tk.Frame(self.root, bg=self.theme["bg"])
        top_frame.pack(fill="x", padx=10, pady=10)

        title = tk.Label(
            top_frame,
            text="🧠 Mental Awareness Companion",
            font=("Helvetica", 18, "bold"),
            bg=self.theme["bg"]
        )

        title.pack(side="left")

        # ==========================
        # CHAT AREA
        # ==========================

        self.chat_area = ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Arial", 11),
            state="disabled",
            padx=10,
            pady=10
        )

        self.chat_area.pack(fill="both", expand=True, padx=10, pady=5)

        # ==========================
        # DAILY CHECK-IN FRAME
        # ==========================

        checkin_frame = tk.LabelFrame(
            self.root,
            text="Daily Check-In",
            padx=10,
            pady=10
        )

        checkin_frame.pack(fill="x", padx=10, pady=5)

        moods = ["😊 Happy", "😌 Calm", "😟 Anxious", "😔 Sad", "😠 Angry"]

        self.mood_var = tk.StringVar()
        self.mood_var.set(moods[0])

        mood_dropdown = ttk.Combobox(
            checkin_frame,
            textvariable=self.mood_var,
            values=moods,
            state="readonly"
        )

        mood_dropdown.pack(side="left", padx=5)

        mood_button = ttk.Button(
            checkin_frame,
            text="Submit Mood",
            command=self.submit_mood
        )

        mood_button.pack(side="left", padx=5)

        # ==========================
        # MINDFULNESS TIMER FRAME
        # ==========================

        timer_frame = tk.LabelFrame(
            self.root,
            text="Mindfulness Timer",
            padx=10,
            pady=10
        )

        timer_frame.pack(fill="x", padx=10, pady=5)

        self.timer_label = tk.Label(
            timer_frame,
            text="60",
            font=("Helvetica", 18, "bold")
        )

        self.timer_label.pack(side="left", padx=10)

        timer_button = ttk.Button(
            timer_frame,
            text="Start Breathing Timer",
            command=self.start_timer
        )

        timer_button.pack(side="left", padx=10)

        # ==========================
        # INPUT FRAME
        # ==========================

        input_frame = tk.Frame(self.root, bg=self.theme["bg"])
        input_frame.pack(fill="x", padx=10, pady=10)

        self.user_input = tk.Entry(
            input_frame,
            font=("Arial", 12)
        )

        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        )

        send_button.pack(side="right")

    # ========================================================
    # THEME MANAGEMENT
    # ========================================================

    def apply_theme(self):
        """Apply current theme colors."""

        self.root.configure(bg=self.theme["bg"])

        self.chat_area.configure(
            bg=self.theme["chat_bg"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"]
        )

    def toggle_theme(self):
        """Switch between dark and light mode."""

        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.theme = self.dark_theme
        else:
            self.theme = self.light_theme

        self.apply_theme()

    # ========================================================
    # CHAT FUNCTIONS
    # ========================================================

    def add_message(self, sender, message, tag):
        """Insert styled message into chat area."""

        self.chat_area.config(state="normal")

        timestamp = current_time()

        formatted = f"[{timestamp}] {sender}: {message}\n\n"

        self.chat_area.insert(tk.END, formatted, tag)

        self.chat_area.tag_config(
            "user",
            background=self.theme["user"],
            foreground=self.theme["text"],
            spacing3=10
        )

        self.chat_area.tag_config(
            "bot",
            background=self.theme["bot"],
            foreground=self.theme["text"],
            spacing3=10
        )

        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)

    def display_bot_message(self, message):
        """Display bot response with typing effect."""

        self.chat_area.config(state="normal")

        timestamp = current_time()

        intro = f"[{timestamp}] Companion: "

        self.chat_area.insert(tk.END, intro, "bot")

        self.typing_effect(message, 0)

    def typing_effect(self, message, index):
        """Typing animation effect."""

        if index < len(message):
            self.chat_area.insert(tk.END, message[index], "bot")
            self.chat_area.see(tk.END)

            self.root.after(
                20,
                lambda: self.typing_effect(message, index + 1)
            )

        else:
            self.chat_area.insert(tk.END, "\n\n")
            self.chat_area.config(state="disabled")

    def send_message(self):
        """Handle user message."""

        text = self.user_input.get().strip()

        if not text:
            return

        # Show user message
        self.add_message("You", text, "user")

        # Clear input
        self.user_input.delete(0, tk.END)

        # Get bot response
        response = self.bot.get_response(text)

        # Display response
        self.display_bot_message(response)

    # ========================================================
    # DAILY CHECK-IN
    # ========================================================

    def submit_mood(self):
        """Handle daily mood check-in."""

        mood = self.mood_var.get()

        responses = {
            "😊 Happy": "It's great to hear you're feeling happy today!",
            "😌 Calm": "A calm mind is valuable. Keep nurturing that peace.",
            "😟 Anxious": "Try a few slow breaths. You deserve moments of calm.",
            "😔 Sad": "It's okay to have difficult emotions. Be gentle with yourself.",
            "😠 Angry": "Taking a short pause may help you process your feelings."
        }

        self.display_bot_message(responses.get(mood))

    # ========================================================
    # MINDFULNESS TIMER
    # ========================================================

    def start_timer(self):
        """Start mindfulness countdown timer."""

        if not self.timer_running:
            self.timer_running = True
            self.timer_seconds = 60
            self.run_timer()

    def run_timer(self):
        """Countdown logic."""

        if self.timer_seconds >= 0:

            self.timer_label.config(text=str(self.timer_seconds))

            self.timer_seconds -= 1

            self.root.after(1000, self.run_timer)

        else:
            self.timer_running = False

            self.display_bot_message(
                "Great job taking a mindfulness break 🌿"
            )

    # ========================================================
    # MENU FUNCTIONS
    # ========================================================

    def export_chat(self):
        """Export chat history."""

        content = self.chat_area.get("1.0", tk.END)

        save_to_file(content)

    def clear_chat(self):
        """Clear chat window."""

        self.chat_area.config(state="normal")
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state="disabled")


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MentalAwarenessApp(root)

    root.mainloop()


"""
============================================================
HOW TO RUN THE APPLICATION
============================================================

1. Make sure Python 3 is installed.
2. Save this file as:
       mental_awareness_companion.py

3. Open terminal or command prompt.

4. Run:
       python mental_awareness_companion.py

============================================================
KEYBOARD SHORTCUTS
============================================================

Enter      -> Send Message
Ctrl + S   -> Save Chat
Ctrl + L   -> Clear Chat

============================================================
FUTURE IMPROVEMENTS
============================================================

- Add sentiment analysis
- Add SQLite database storage
- Add voice input/output
- Add animated UI themes
- Add emotion tracking charts
- Add personalized wellness reminders
- Add multilingual support
- Add secure encrypted journaling

============================================================
OPTIONAL ENHANCEMENTS
============================================================

- Integrate NLP libraries like NLTK or TextBlob
- Add AI-powered conversation memory
- Add daily affirmation notifications
- Add wellness progress analytics
- Add user profiles and settings

============================================================
IMPORTANT NOTE
============================================================

This application is designed for emotional support
and mindfulness awareness only.

It is NOT a replacement for professional mental
health care, diagnosis, or emergency services.
"""
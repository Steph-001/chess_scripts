import tkinter as tk
from tkinter import messagebox
import random
import time


class ChessTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Trainer")
        self.root.geometry("500x680")

        # Training state
        self.training_active = False
        self.current_streak = 0
        self.highest_streak = 0
        self.start_time = None
        self.duration_seconds = 0
        self.drill_type = None

        # Setup menubar
        self.setup_menubar()

        # Setup UI
        self.setup_start_screen()

    def setup_menubar(self):
        """Create the application menubar"""
        menubar = tk.Menu(self.root)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Drill Descriptions", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def show_help(self):
        """Show help window with drill descriptions"""
        help_win = tk.Toplevel(self.root)
        help_win.title("Drill Descriptions")
        help_win.geometry("560x520")
        help_win.transient(self.root)
        help_win.grab_set()

        tk.Label(help_win, text="Drill Descriptions", font=("Arial", 16, "bold")).pack(pady=(15, 10))

        # Scrollable frame
        container = tk.Frame(help_win)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        drills = [
            ("Square Color",
             "A square is shown (e.g. e4). You answer whether it's dark or light. "
             "Trains instant square color recognition — a fundamental blindfold skill."),

            ("Queen and Bishop",
             "A black queen and white bishop are placed on the board with a target square. "
             "Find how the bishop reaches the target in 2 moves while avoiding the queen's control. "
             "The target is always the same color as the bishop and not on its current diagonal."),

            ("Queen and Knight",
             "A black queen and white knight are placed on the board with a target square. "
             "Visualize how the knight navigates to the target while the queen controls part of the board."),

            ("R+B vs Bishop",
             "A black rook and bishop face a white bishop. A target square is given. "
             "Find the route for the white bishop to reach the target while avoiding enemy piece control."),

            ("R+B vs Knight",
             "A black rook and bishop face a white knight. A target square is given. "
             "Find the route for the white knight to reach the target while avoiding enemy piece control."),

            ("Bishop vs Pawn",
             "A pawn races to promote while a bishop tries to intercept it. "
             "Determine whether the bishop can catch the pawn before it queens. "
             "The turn to move is specified."),

            ("Knight vs Pawn",
             "Same as Bishop vs Pawn but with a knight. "
             "Determine whether the knight can catch the pawn before it queens. "
             "Knight distances are less intuitive — good calculation practice."),

            ("Bishop Route",
             "Five squares of the same color are shown as a route. For each consecutive pair, "
             "the bishop needs exactly 2 moves. Find the connecting intermediate square(s). "
             "There can be 1 or 2 possible connecting squares per leg. Untimed."),

            ("Knight Route",
             "Three squares are shown as a route. For each consecutive pair, "
             "the knight needs exactly 2 moves with only 1 possible intermediate square. "
             "Find the connecting square for each leg. Untimed."),

            ("Intersection",
             "Five questions ask where a file or rank intersects a diagonal. "
             "Diagonals are named by their endpoints (e.g. a8-h1). "
             "Endpoint squares are excluded — you must visualize the interior of the diagonal. "
             "Sometimes the answer is 'no intersection'. Untimed."),
        ]

        for i, (name, desc) in enumerate(drills):
            frame = tk.Frame(scroll_frame)
            frame.pack(fill=tk.X, pady=(0, 8), padx=5)

            tk.Label(frame, text=name, font=("Arial", 12, "bold"),
                     fg="#1565C0", anchor="w").pack(fill=tk.X)
            tk.Label(frame, text=desc, font=("Arial", 11), wraplength=500,
                     justify=tk.LEFT, anchor="w").pack(fill=tk.X)

            if i < len(drills) - 1:
                tk.Frame(frame, height=1, bg="#CCCCCC").pack(fill=tk.X, pady=(6, 0))

        # Close button
        tk.Button(help_win, text="Close", font=("Arial", 12),
                  command=help_win.destroy, bg="#2196F3", fg="black",
                  width=10).pack(pady=10)

    def show_about(self):
        """Show about dialog"""
        about_win = tk.Toplevel(self.root)
        about_win.title("About")
        about_win.geometry("300x150")
        about_win.transient(self.root)
        about_win.grab_set()

        tk.Label(about_win, text="Chess Trainer", font=("Arial", 16, "bold")).pack(pady=(20, 5))
        tk.Label(about_win, text="Blindfold chess visualization drills",
                 font=("Arial", 11), fg="#555555").pack(pady=5)
        tk.Button(about_win, text="OK", font=("Arial", 11),
                  command=about_win.destroy, width=8).pack(pady=15)

    def setup_start_screen(self):
        """Initial screen to set duration and start training"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("500x680")

        # Title
        title = tk.Label(self.root, text="Chess Training Drills", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Duration selection
        duration_frame = tk.Frame(self.root)
        duration_frame.pack(pady=20)

        tk.Label(duration_frame, text="Duration (minutes):", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.duration_var = tk.StringVar(value="5")
        duration_entry = tk.Entry(duration_frame, textvariable=self.duration_var, width=10, font=("Arial", 12))
        duration_entry.pack(side=tk.LEFT, padx=5)

        # Drill selection buttons
        tk.Label(self.root, text="Select Drill:", font=("Arial", 14, "bold")).pack(pady=(20, 10))

        # First row of buttons
        button_frame1 = tk.Frame(self.root)
        button_frame1.pack(pady=10)

        square_color_btn = tk.Button(button_frame1, text="Square Color", font=("Arial", 14),
                                     command=lambda: self.start_training("square_color"),
                                     bg="#4CAF50", fg="black", width=15, height=2)
        square_color_btn.pack(side=tk.LEFT, padx=10)

        queen_bishop_btn = tk.Button(button_frame1, text="Queen and Bishop", font=("Arial", 14),
                                     command=lambda: self.start_training("queen_bishop"),
                                     bg="#00BCD4", fg="black", width=15, height=2)
        queen_bishop_btn.pack(side=tk.LEFT, padx=10)

        # Second row of buttons
        button_frame2 = tk.Frame(self.root)
        button_frame2.pack(pady=10)

        queen_knight_btn = tk.Button(button_frame2, text="Queen and Knight", font=("Arial", 14),
                                     command=lambda: self.start_training("queen_knight"),
                                     bg="#2196F3", fg="black", width=15, height=2)
        queen_knight_btn.pack(side=tk.LEFT, padx=10)

        rook_bishop_bishop_btn = tk.Button(button_frame2, text="R+B vs Bishop", font=("Arial", 14),
                                           command=lambda: self.start_training("rb_bishop"),
                                           bg="#E91E63", fg="black", width=15, height=2)
        rook_bishop_bishop_btn.pack(side=tk.LEFT, padx=10)

        # Third row of buttons
        button_frame3 = tk.Frame(self.root)
        button_frame3.pack(pady=10)

        rook_bishop_knight_btn = tk.Button(button_frame3, text="R+B vs Knight", font=("Arial", 14),
                                           command=lambda: self.start_training("rb_knight"),
                                           bg="#795548", fg="black", width=15, height=2)
        rook_bishop_knight_btn.pack(side=tk.LEFT, padx=10)

        bishop_pawn_btn = tk.Button(button_frame3, text="Bishop vs Pawn", font=("Arial", 14),
                                    command=lambda: self.start_training("bishop_pawn"),
                                    bg="#FF9800", fg="black", width=15, height=2)
        bishop_pawn_btn.pack(side=tk.LEFT, padx=10)

        # Fourth row of buttons
        button_frame4 = tk.Frame(self.root)
        button_frame4.pack(pady=10)

        knight_pawn_btn = tk.Button(button_frame4, text="Knight vs Pawn", font=("Arial", 14),
                                    command=lambda: self.start_training("knight_pawn"),
                                    bg="#9C27B0", fg="black", width=15, height=2)
        knight_pawn_btn.pack(side=tk.LEFT, padx=10)

        bishop_route_btn = tk.Button(button_frame4, text="Bishop Route", font=("Arial", 14),
                                     command=lambda: self.start_training("bishop_route"),
                                     bg="#607D8B", fg="black", width=15, height=2)
        bishop_route_btn.pack(side=tk.LEFT, padx=10)

        # Fifth row of buttons
        button_frame5 = tk.Frame(self.root)
        button_frame5.pack(pady=10)

        knight_route_btn = tk.Button(button_frame5, text="Knight Route", font=("Arial", 14),
                                     command=lambda: self.start_training("knight_route"),
                                     bg="#3F51B5", fg="black", width=15, height=2)
        knight_route_btn.pack(side=tk.LEFT, padx=10)

        intersection_btn = tk.Button(button_frame5, text="Intersection", font=("Arial", 14),
                                     command=lambda: self.start_training("intersection"),
                                     bg="#FF5722", fg="black", width=15, height=2)
        intersection_btn.pack(side=tk.LEFT, padx=10)

        # Help button
        help_btn = tk.Button(self.root, text="?  Help", font=("Arial", 12),
                             command=self.show_help, bg="#BDBDBD", fg="black",
                             width=10, height=1)
        help_btn.pack(pady=(15, 5))

    def start_training(self, drill_type):
        """Begin the training session"""
        # Only square_color is timed
        if drill_type == "square_color":
            try:
                duration_minutes = float(self.duration_var.get())
                if duration_minutes <= 0:
                    raise ValueError("Duration must be positive")
                self.duration_seconds = duration_minutes * 60
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid positive number for duration")
                return

        # Reset stats
        self.current_streak = 0
        self.highest_streak = 0
        self.training_active = True
        self.start_time = time.time()
        self.drill_type = drill_type

        # Setup appropriate training screen
        if drill_type == "square_color":
            self.setup_square_color_screen()
            self.show_new_square()
        elif drill_type == "queen_bishop":
            self.setup_queen_bishop_screen()
            self.show_new_queen_bishop()
        elif drill_type == "queen_knight":
            self.setup_queen_knight_screen()
            self.show_new_queen_knight()
        elif drill_type == "rb_bishop":
            self.setup_rb_bishop_screen()
            self.show_new_rb_bishop()
        elif drill_type == "rb_knight":
            self.setup_rb_knight_screen()
            self.show_new_rb_knight()
        elif drill_type == "bishop_pawn":
            self.setup_piece_pawn_screen("bishop")
            self.show_new_piece_pawn("bishop")
        elif drill_type == "knight_pawn":
            self.setup_piece_pawn_screen("knight")
            self.show_new_piece_pawn("knight")
        elif drill_type == "bishop_route":
            self.setup_bishop_route_screen()
            self.show_new_bishop_route()
        elif drill_type == "knight_route":
            self.setup_knight_route_screen()
            self.show_new_knight_route()
        elif drill_type == "intersection":
            self.setup_intersection_screen()
            self.show_new_intersection_set()

        # Only square_color uses the timer
        if drill_type == "square_color":
            self.check_time()

    # ==================== SQUARE COLOR DRILL ====================

    def setup_square_color_screen(self):
        """Setup the square color training interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("400x420")

        # Square display
        self.square_label = tk.Label(self.root, text="", font=("Arial", 48, "bold"), fg="black")
        self.square_label.pack(pady=40)

        # Streak display
        self.streak_label = tk.Label(self.root, text="Current streak: 0 | Best: 0", font=("Arial", 12))
        self.streak_label.pack(pady=10)

        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.dark_btn = tk.Button(button_frame, text="Dark", font=("Arial", 16),
                                  command=lambda: self.check_answer("dark"),
                                  bg="#8B7355", fg="black", width=10, height=2)
        self.dark_btn.pack(side=tk.LEFT, padx=10)

        self.light_btn = tk.Button(button_frame, text="Light", font=("Arial", 16),
                                   command=lambda: self.check_answer("light"),
                                   bg="#FFE4B5", fg="black", width=10, height=2)
        self.light_btn.pack(side=tk.LEFT, padx=10)

        # Time remaining label
        self.time_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.time_label.pack(pady=5)

        # Abort button
        tk.Button(self.root, text="← Abort", font=("Arial", 10),
                  command=self.abort_training, bg="#9E9E9E", fg="black",
                  width=10).pack(pady=5)

    def show_new_square(self):
        """Display a random chess square"""
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

        self.current_file = random.choice(files)
        self.current_rank = random.choice(ranks)
        self.current_square = self.current_file + self.current_rank

        self.square_label.config(text=self.current_square)

    def get_square_color(self, square):
        """Determine if a square is dark or light"""
        file_num = ord(square[0]) - ord('a') + 1  # a=1, b=2, etc.
        rank_num = int(square[1])

        # If sum is even, square is dark; if odd, square is light
        return "dark" if (file_num + rank_num) % 2 == 0 else "light"

    def check_answer(self, answer):
        """Check if the answer is correct"""
        if not self.training_active:
            return

        correct_answer = self.get_square_color(self.current_square)

        if answer == correct_answer:
            # Correct answer
            self.current_streak += 1
            if self.current_streak > self.highest_streak:
                self.highest_streak = self.current_streak
            self.update_streak_display()
            self.show_new_square()
        else:
            # Incorrect answer
            self.current_streak = 0
            self.update_streak_display()
            self.show_mistake_message()

    def show_mistake_message(self):
        """Show mistake message and wait for click to continue"""
        # Disable answer buttons
        self.dark_btn.config(state=tk.DISABLED)
        self.light_btn.config(state=tk.DISABLED)

        # Show mistake message
        mistake_window = tk.Toplevel(self.root)
        mistake_window.title("Mistake")
        mistake_window.geometry("400x250")
        mistake_window.transient(self.root)
        mistake_window.grab_set()

        tk.Label(mistake_window, text="Mistake!", font=("Arial", 24, "bold"), fg="red").pack(pady=30)

        correct_answer = self.get_square_color(self.current_square)
        tk.Label(mistake_window, text=f"{self.current_square} is {correct_answer}",
                 font=("Arial", 16)).pack(pady=15)

        def continue_training():
            mistake_window.destroy()
            self.dark_btn.config(state=tk.NORMAL)
            self.light_btn.config(state=tk.NORMAL)
            self.show_new_square()

        tk.Button(mistake_window, text="Continue", font=("Arial", 16, "bold"),
                  command=continue_training, bg="#2196F3", fg="black",
                  width=20, height=3).pack(pady=20)

    def update_streak_display(self):
        """Update the streak labels"""
        self.streak_label.config(text=f"Current streak: {self.current_streak} | Best: {self.highest_streak}")

    # ==================== QUEEN AND KNIGHT DRILL ====================

    def setup_queen_knight_screen(self):
        """Setup the queen and knight training interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("500x400")

        # Title
        tk.Label(self.root, text="Queen and Knight Drill", font=("Arial", 18, "bold")).pack(pady=20)

        # Positions display frame
        positions_frame = tk.Frame(self.root)
        positions_frame.pack(pady=20)

        # Black Queen
        tk.Label(positions_frame, text="♛ Black Queen:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.queen_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#8B008B")
        self.queen_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # White Knight
        tk.Label(positions_frame, text="♘ White Knight:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.knight_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#4169E1")
        self.knight_label.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Target square
        tk.Label(positions_frame, text="🎯 Target:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.target_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#228B22")
        self.target_label.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Next button
        self.next_btn = tk.Button(self.root, text="Next Position", font=("Arial", 14),
                                  command=self.show_new_queen_knight,
                                  bg="#4CAF50", fg="black", width=15, height=2)
        self.next_btn.pack(pady=20)

        # Back button
        tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                  command=self.abort_training, bg="#9E9E9E", fg="black",
                  width=14, height=1).pack(pady=5)

    def is_queen_attacking_square(self, queen_square, target_square):
        """Check if queen attacks a target square"""
        q_file, q_rank = ord(queen_square[0]) - ord('a'), int(queen_square[1]) - 1
        t_file, t_rank = ord(target_square[0]) - ord('a'), int(target_square[1]) - 1

        # Same file or rank
        if q_file == t_file or q_rank == t_rank:
            return True

        # Diagonal
        if abs(q_file - t_file) == abs(q_rank - t_rank):
            return True

        return False

    def show_new_queen_knight(self):
        """Generate and display new queen and knight positions"""
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

        # Generate random queen position
        queen_file = random.choice(files)
        queen_rank = random.choice(ranks)
        queen_square = queen_file + queen_rank

        # Generate knight position (not controlled by queen)
        while True:
            knight_file = random.choice(files)
            knight_rank = random.choice(ranks)
            knight_square = knight_file + knight_rank

            if knight_square != queen_square and not self.is_queen_attacking_square(queen_square, knight_square):
                break

        # Generate target square (different from queen and knight)
        while True:
            target_file = random.choice(files)
            target_rank = random.choice(ranks)
            target_square = target_file + target_rank

            if target_square != queen_square and target_square != knight_square:
                break

        # Update labels
        self.queen_label.config(text=queen_square)
        self.knight_label.config(text=knight_square)
        self.target_label.config(text=target_square)

    # ==================== QUEEN AND BISHOP DRILL ====================

    def setup_queen_bishop_screen(self):
        """Setup the queen and bishop training interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("500x400")

        # Title
        tk.Label(self.root, text="Queen and Bishop Drill", font=("Arial", 18, "bold")).pack(pady=20)

        # Positions display frame
        positions_frame = tk.Frame(self.root)
        positions_frame.pack(pady=20)

        # Black Queen
        tk.Label(positions_frame, text="♛ Black Queen:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.queen_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#8B008B")
        self.queen_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # White Bishop
        tk.Label(positions_frame, text="♗ White Bishop:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.bishop_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#8B4513")
        self.bishop_label.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Target square
        tk.Label(positions_frame, text="🎯 Target:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.target_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#228B22")
        self.target_label.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Next button
        self.next_btn = tk.Button(self.root, text="Next Position", font=("Arial", 14),
                                  command=self.show_new_queen_bishop,
                                  bg="#4CAF50", fg="black", width=15, height=2)
        self.next_btn.pack(pady=20)

        # Back button
        tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                  command=self.abort_training, bg="#9E9E9E", fg="black",
                  width=14, height=1).pack(pady=5)

    def get_square_color_numeric(self, square):
        """Get numeric square color (0 or 1)"""
        file_num = ord(square[0]) - ord('a')
        rank_num = int(square[1]) - 1
        return (file_num + rank_num) % 2

    def show_new_queen_bishop(self):
        """Generate and display new queen and bishop positions"""
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

        # Generate random queen position
        queen_file = random.choice(files)
        queen_rank = random.choice(ranks)
        queen_square = queen_file + queen_rank

        # Generate bishop position (not controlled by queen)
        while True:
            bishop_file = random.choice(files)
            bishop_rank = random.choice(ranks)
            bishop_square = bishop_file + bishop_rank

            if bishop_square != queen_square and not self.is_queen_attacking_square(queen_square, bishop_square):
                break

        # Get bishop's square color
        bishop_color = self.get_square_color_numeric(bishop_square)

        # Generate target square (same color as bishop, different from queen and bishop, NOT reachable in 1 move)
        while True:
            target_file = random.choice(files)
            target_rank = random.choice(ranks)
            target_square = target_file + target_rank
            target_color = self.get_square_color_numeric(target_square)

            # Check if bishop can reach target in one move (same diagonal)
            b_file, b_rank = ord(bishop_square[0]) - ord('a'), int(bishop_square[1]) - 1
            t_file, t_rank = ord(target_square[0]) - ord('a'), int(target_square[1]) - 1
            on_same_diagonal = abs(b_file - t_file) == abs(b_rank - t_rank)

            if (target_square != queen_square and
                target_square != bishop_square and
                target_color == bishop_color and
                not on_same_diagonal):  # Ensure it takes at least 2 moves
                break

        # Update labels
        self.queen_label.config(text=queen_square)
        self.bishop_label.config(text=bishop_square)
        self.target_label.config(text=target_square)

    # ==================== ROOK+BISHOP VS BISHOP DRILL ====================

    def setup_rb_bishop_screen(self):
        """Setup the rook+bishop vs bishop training interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("500x450")

        # Title
        tk.Label(self.root, text="Rook + Bishop vs Bishop", font=("Arial", 18, "bold")).pack(pady=20)

        # Positions display frame
        positions_frame = tk.Frame(self.root)
        positions_frame.pack(pady=20)

        # Black Rook
        tk.Label(positions_frame, text="♜ Black Rook:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.rook_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#8B0000")
        self.rook_label.grid(row=0, column=1, sticky="w", padx=10, pady=8)

        # Black Bishop
        tk.Label(positions_frame, text="♝ Black Bishop:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.black_bishop_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#4B0082")
        self.black_bishop_label.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        # White Bishop
        tk.Label(positions_frame, text="♗ White Bishop:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.white_bishop_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#8B4513")
        self.white_bishop_label.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        # Target square
        tk.Label(positions_frame, text="🎯 Target:", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.target_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#228B22")
        self.target_label.grid(row=3, column=1, sticky="w", padx=10, pady=8)

        # Next button
        self.next_btn = tk.Button(self.root, text="Next Position", font=("Arial", 14),
                                  command=self.show_new_rb_bishop,
                                  bg="#4CAF50", fg="black", width=15, height=2)
        self.next_btn.pack(pady=20)

        # Back button
        tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                  command=self.abort_training, bg="#9E9E9E", fg="black",
                  width=14, height=1).pack(pady=5)

    def is_rook_attacking_square(self, rook_square, target_square):
        """Check if rook attacks a target square"""
        r_file, r_rank = ord(rook_square[0]) - ord('a'), int(rook_square[1]) - 1
        t_file, t_rank = ord(target_square[0]) - ord('a'), int(target_square[1]) - 1

        # Same file or rank
        if r_file == t_file or r_rank == t_rank:
            return True

        return False

    def is_bishop_attacking_square(self, bishop_square, target_square):
        """Check if bishop attacks a target square"""
        b_file, b_rank = ord(bishop_square[0]) - ord('a'), int(bishop_square[1]) - 1
        t_file, t_rank = ord(target_square[0]) - ord('a'), int(target_square[1]) - 1

        # Diagonal
        if abs(b_file - t_file) == abs(b_rank - t_rank):
            return True

        return False

    def show_new_rb_bishop(self):
        """Generate and display new rook+bishop vs bishop positions"""
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

        # Generate random black rook position
        rook_file = random.choice(files)
        rook_rank = random.choice(ranks)
        rook_square = rook_file + rook_rank

        # Generate random black bishop position (different from rook)
        while True:
            black_bishop_file = random.choice(files)
            black_bishop_rank = random.choice(ranks)
            black_bishop_square = black_bishop_file + black_bishop_rank

            if black_bishop_square != rook_square:
                break

        # Generate white bishop position (not controlled by rook or black bishop)
        while True:
            white_bishop_file = random.choice(files)
            white_bishop_rank = random.choice(ranks)
            white_bishop_square = white_bishop_file + white_bishop_rank

            if (white_bishop_square != rook_square and
                white_bishop_square != black_bishop_square and
                not self.is_rook_attacking_square(rook_square, white_bishop_square) and
                not self.is_bishop_attacking_square(black_bishop_square, white_bishop_square)):
                break

        # Get white bishop's square color
        white_bishop_color = self.get_square_color_numeric(white_bishop_square)

        # Generate target square (same color as white bishop, different from all pieces)
        while True:
            target_file = random.choice(files)
            target_rank = random.choice(ranks)
            target_square = target_file + target_rank
            target_color = self.get_square_color_numeric(target_square)

            if (target_square != rook_square and
                target_square != black_bishop_square and
                target_square != white_bishop_square and
                target_color == white_bishop_color):
                break

        # Update labels
        self.rook_label.config(text=rook_square)
        self.black_bishop_label.config(text=black_bishop_square)
        self.white_bishop_label.config(text=white_bishop_square)
        self.target_label.config(text=target_square)

    # ==================== ROOK+BISHOP VS KNIGHT DRILL ====================

    def setup_rb_knight_screen(self):
        """Setup the rook+bishop vs knight training interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("500x450")

        # Title
        tk.Label(self.root, text="Rook + Bishop vs Knight", font=("Arial", 18, "bold")).pack(pady=20)

        # Positions display frame
        positions_frame = tk.Frame(self.root)
        positions_frame.pack(pady=20)

        # Black Rook
        tk.Label(positions_frame, text="♜ Black Rook:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.rook_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#8B0000")
        self.rook_label.grid(row=0, column=1, sticky="w", padx=10, pady=8)

        # Black Bishop
        tk.Label(positions_frame, text="♝ Black Bishop:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.black_bishop_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#4B0082")
        self.black_bishop_label.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        # White Knight
        tk.Label(positions_frame, text="♘ White Knight:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.white_knight_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#4169E1")
        self.white_knight_label.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        # Target square
        tk.Label(positions_frame, text="🎯 Target:", font=("Arial", 14)).grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.target_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#228B22")
        self.target_label.grid(row=3, column=1, sticky="w", padx=10, pady=8)

        # Next button
        self.next_btn = tk.Button(self.root, text="Next Position", font=("Arial", 14),
                                  command=self.show_new_rb_knight,
                                  bg="#4CAF50", fg="black", width=15, height=2)
        self.next_btn.pack(pady=20)

        # Back button
        tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                  command=self.abort_training, bg="#9E9E9E", fg="black",
                  width=14, height=1).pack(pady=5)

    def show_new_rb_knight(self):
        """Generate and display new rook+bishop vs knight positions"""
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

        # Generate random black rook position
        rook_file = random.choice(files)
        rook_rank = random.choice(ranks)
        rook_square = rook_file + rook_rank

        # Generate random black bishop position (different from rook)
        while True:
            black_bishop_file = random.choice(files)
            black_bishop_rank = random.choice(ranks)
            black_bishop_square = black_bishop_file + black_bishop_rank

            if black_bishop_square != rook_square:
                break

        # Generate white knight position (not controlled by rook or black bishop)
        while True:
            white_knight_file = random.choice(files)
            white_knight_rank = random.choice(ranks)
            white_knight_square = white_knight_file + white_knight_rank

            if (white_knight_square != rook_square and
                white_knight_square != black_bishop_square and
                not self.is_rook_attacking_square(rook_square, white_knight_square) and
                not self.is_bishop_attacking_square(black_bishop_square, white_knight_square)):
                break

        # Generate target square (any square, different from all pieces)
        while True:
            target_file = random.choice(files)
            target_rank = random.choice(ranks)
            target_square = target_file + target_rank

            if (target_square != rook_square and
                target_square != black_bishop_square and
                target_square != white_knight_square):
                break

        # Update labels
        self.rook_label.config(text=rook_square)
        self.black_bishop_label.config(text=black_bishop_square)
        self.white_knight_label.config(text=white_knight_square)
        self.target_label.config(text=target_square)

    # ==================== PIECE VS PAWN DRILL (BISHOP/KNIGHT) ====================

    def setup_piece_pawn_screen(self, piece_type):
        """Setup the piece vs pawn training interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("500x400")

        piece_name = piece_type.capitalize()

        # Title
        tk.Label(self.root, text=f"{piece_name} vs Pawn Race", font=("Arial", 16, "bold")).pack(pady=20)

        # Positions display frame
        positions_frame = tk.Frame(self.root)
        positions_frame.pack(pady=20)

        # Pawn
        tk.Label(positions_frame, text="Pawn:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.pawn_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#2F4F4F")
        self.pawn_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Piece
        tk.Label(positions_frame, text=f"{piece_name}:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.piece_label = tk.Label(positions_frame, text="", font=("Arial", 20, "bold"), fg="#8B4513")
        self.piece_label.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Turn indicator
        tk.Label(positions_frame, text="To move:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.turn_label = tk.Label(positions_frame, text="", font=("Arial", 18, "bold"), fg="#0000CD")
        self.turn_label.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Next button
        self.next_btn = tk.Button(self.root, text="Next Position", font=("Arial", 14),
                                  command=lambda: self.show_new_piece_pawn(piece_type),
                                  bg="#4CAF50", fg="black", width=15, height=2)
        self.next_btn.pack(pady=20)

        # Show answer button
        self.answer_btn = tk.Button(self.root, text="Show Answer", font=("Arial", 12),
                                    command=lambda: self.show_piece_pawn_answer(piece_type),
                                    bg="#2196F3", fg="black", width=15, height=1)
        self.answer_btn.pack(pady=5)

        # Back button
        tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                  command=self.abort_training, bg="#9E9E9E", fg="black",
                  width=14, height=1).pack(pady=5)

    def generate_piece_pawn_position(self):
        """Generate a random pawn and piece position"""
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Random pawn color
        pawn_color = random.choice(['white', 'black'])

        # Random file for pawn
        pawn_file = random.choice(files)

        # Pawn rank: specified ranks based on color
        if pawn_color == 'white':
            pawn_rank = random.choice(['4', '5', '6'])
        else:
            pawn_rank = random.choice(['3', '4', '5'])

        pawn_square = pawn_file + pawn_rank

        # Random piece position (not same square as pawn)
        while True:
            piece_file = random.choice(files)
            piece_rank = random.choice(['1', '2', '3', '4', '5', '6', '7', '8'])
            piece_square = piece_file + piece_rank
            if piece_square != pawn_square:
                break

        # Random turn
        to_move = random.choice(['piece', 'pawn'])

        return pawn_square, pawn_color, piece_square, to_move

    def show_new_piece_pawn(self, piece_type):
        """Display new piece vs pawn position"""
        self.pawn_square, self.pawn_color, self.piece_square, self.to_move = self.generate_piece_pawn_position()

        # Update labels
        pawn_symbol = "♟"
        pawn_color_text = "White" if self.pawn_color == 'white' else "Black"
        self.pawn_label.config(text=f"{pawn_symbol} {pawn_color_text} {self.pawn_square}")

        piece_symbol = "♗" if piece_type == "bishop" else "♘"
        self.piece_label.config(text=f"{piece_symbol} {self.piece_square}")

        to_move_text = piece_type.capitalize() if self.to_move == 'piece' else 'Pawn'
        self.turn_label.config(text=to_move_text)

    def calculate_bishop_moves_to_square(self, bishop_pos, target_pos):
        """Calculate minimum moves for bishop to reach target square"""
        b_file, b_rank = ord(bishop_pos[0]) - ord('a'), int(bishop_pos[1]) - 1
        t_file, t_rank = ord(target_pos[0]) - ord('a'), int(target_pos[1]) - 1

        # If already on target
        if bishop_pos == target_pos:
            return 0

        # Check if target is on same diagonal
        if abs(b_file - t_file) == abs(b_rank - t_rank):
            return 1

        # Check if target is same color square as bishop
        bishop_square_color = (b_file + b_rank) % 2
        target_square_color = (t_file + t_rank) % 2

        if bishop_square_color != target_square_color:
            return float('inf')  # Impossible - different colored squares

        # Otherwise it takes 2 moves
        return 2

    def calculate_knight_moves_to_square(self, knight_pos, target_pos):
        """Calculate minimum moves for knight to reach target square"""
        from collections import deque

        if knight_pos == target_pos:
            return 0

        k_file, k_rank = ord(knight_pos[0]) - ord('a'), int(knight_pos[1]) - 1
        t_file, t_rank = ord(target_pos[0]) - ord('a'), int(target_pos[1]) - 1

        # BFS to find shortest path
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        visited = set()
        queue = deque([(k_file, k_rank, 0)])
        visited.add((k_file, k_rank))

        while queue:
            file, rank, moves = queue.popleft()

            if file == t_file and rank == t_rank:
                return moves

            for df, dr in knight_moves:
                new_file, new_rank = file + df, rank + dr
                if 0 <= new_file < 8 and 0 <= new_rank < 8 and (new_file, new_rank) not in visited:
                    visited.add((new_file, new_rank))
                    queue.append((new_file, new_rank, moves + 1))

        return float('inf')

    def can_piece_catch_pawn(self, piece_type):
        """Determine if piece can catch the pawn before it queens"""
        pawn_file = self.pawn_square[0]
        pawn_rank = int(self.pawn_square[1])

        # Determine promotion rank and pawn direction
        if self.pawn_color == 'white':
            promotion_rank = 8
            direction = 1
        else:
            promotion_rank = 1
            direction = -1

        # Calculate squares pawn will occupy
        pawn_path = []
        current_rank = pawn_rank
        while current_rank != promotion_rank:
            pawn_path.append(pawn_file + str(current_rank))
            current_rank += direction

        # Check each square in pawn's path
        for i, square in enumerate(pawn_path):
            if piece_type == "bishop":
                moves_for_piece = self.calculate_bishop_moves_to_square(self.piece_square, square)
            else:  # knight
                moves_for_piece = self.calculate_knight_moves_to_square(self.piece_square, square)

            # Calculate piece moves available when pawn reaches this square
            if self.to_move == 'pawn':
                piece_moves_available = (i + 1 + 1) // 2
            else:
                piece_moves_available = i + 1

            if moves_for_piece <= piece_moves_available and i < len(pawn_path) - 1:
                return True, square

        return False, None

    def show_piece_pawn_answer(self, piece_type):
        """Show the answer in a popup"""
        can_catch, capture_square = self.can_piece_catch_pawn(piece_type)

        answer_window = tk.Toplevel(self.root)
        answer_window.title("Answer")
        answer_window.geometry("350x200")
        answer_window.transient(self.root)
        answer_window.grab_set()

        piece_name = piece_type.capitalize()

        if can_catch:
            result_text = "YES"
            result_color = "#4CAF50"
            detail_text = f"{piece_name} can capture on {capture_square}"
        else:
            result_text = "NO"
            result_color = "#F44336"
            detail_text = "Pawn will queen"

        tk.Label(answer_window, text=result_text, font=("Arial", 32, "bold"),
                 fg=result_color).pack(pady=20)
        tk.Label(answer_window, text=detail_text, font=("Arial", 14)).pack(pady=10)

        tk.Button(answer_window, text="OK", font=("Arial", 14),
                  command=answer_window.destroy, bg="#2196F3", fg="black",
                  width=10, height=2).pack(pady=20)

    # ==================== BISHOP ROUTE DRILL ====================

    def _sq_to_coords(self, square):
        """Convert algebraic notation to (file, rank) 0-indexed tuple"""
        return ord(square[0]) - ord('a'), int(square[1]) - 1

    def _coords_to_sq(self, file, rank):
        """Convert (file, rank) 0-indexed tuple to algebraic notation"""
        return chr(file + ord('a')) + str(rank + 1)

    def _find_connecting_squares(self, sq_a, sq_b):
        """Find all valid intermediate squares for a bishop moving from sq_a to sq_b in 2 moves.

        An intermediate square must:
        - Be on a diagonal from sq_a (bishop can reach it in 1 move)
        - Be on a diagonal from sq_b (bishop can reach sq_b from it in 1 move)
        - Be on the board (0-7 for both file and rank)
        - Not be sq_a or sq_b themselves
        """
        af, ar = self._sq_to_coords(sq_a)
        bf, br = self._sq_to_coords(sq_b)

        results = []

        # Diagonals from A: (af + t, ar + t), (af + t, ar - t), (af - t, ar + t), (af - t, ar - t)
        # Diagonals from B: similarly
        # Intermediate square must be at intersection of one of A's diagonals with one of B's diagonals.
        # A's diagonals: f - r = af - ar (const) or f + r = af + ar (const)
        # B's diagonals: f - r = bf - br (const) or f + r = bf + br (const)

        a_diag1 = af + ar  # f + r = constant (anti-diagonal)
        a_diag2 = af - ar  # f - r = constant (main diagonal)
        b_diag1 = bf + br
        b_diag2 = bf - br

        # Intersection of A's anti-diag with B's anti-diag: same line, gives all points on that line (not useful, means same diagonal)
        # Intersection of A's anti-diag with B's main-diag:
        #   f + r = a_diag1 and f - r = b_diag2  => f = (a_diag1 + b_diag2) / 2, r = (a_diag1 - b_diag2) / 2
        # Intersection of A's main-diag with B's anti-diag:
        #   f - r = a_diag2 and f + r = b_diag1  => f = (a_diag2 + b_diag1) / 2, r = (b_diag1 - a_diag2) / 2
        # Intersection of A's main-diag with B's main-diag: same line (not useful)

        candidates = []

        # A anti-diag x B main-diag
        f2 = a_diag1 + b_diag2
        r2 = a_diag1 - b_diag2
        if f2 % 2 == 0 and r2 % 2 == 0:
            candidates.append((f2 // 2, r2 // 2))

        # A main-diag x B anti-diag
        f2 = a_diag2 + b_diag1
        r2 = b_diag1 - a_diag2
        if f2 % 2 == 0 and r2 % 2 == 0:
            candidates.append((f2 // 2, r2 // 2))

        for f, r in candidates:
            if 0 <= f <= 7 and 0 <= r <= 7:
                sq = self._coords_to_sq(f, r)
                if sq != sq_a and sq != sq_b:
                    results.append(sq)

        # Deduplicate (shouldn't happen but just in case)
        return sorted(set(results))

    def _generate_bishop_route(self):
        """Generate a route of 5 squares, all same color, no repeats,
        each consecutive pair NOT on the same diagonal (requires 2 moves)."""
        all_squares = [chr(f + ord('a')) + str(r + 1) for f in range(8) for r in range(8)]

        # Pick a random color
        color = random.choice([0, 1])
        same_color_squares = [sq for sq in all_squares if self.get_square_color_numeric(sq) == color]

        max_attempts = 500
        for _ in range(max_attempts):
            route = []
            available = list(same_color_squares)
            random.shuffle(available)

            # Pick first square
            route.append(available.pop())

            success = True
            for step in range(4):
                # Find candidates: same color, not in route, not on same diagonal as last square
                last = route[-1]
                lf, lr = self._sq_to_coords(last)

                candidates = []
                for sq in available:
                    sf, sr = self._sq_to_coords(sq)
                    # Not on same diagonal => not reachable in 1 bishop move
                    if abs(lf - sf) != abs(lr - sr):
                        # Also verify connecting squares exist (at least 1 on the board)
                        connecting = self._find_connecting_squares(last, sq)
                        if len(connecting) >= 1:
                            candidates.append(sq)

                if not candidates:
                    success = False
                    break

                chosen = random.choice(candidates)
                route.append(chosen)
                available.remove(chosen)

            if success and len(route) == 5:
                return route

        # Fallback (should essentially never happen with 32 same-color squares)
        return None

    def setup_bishop_route_screen(self):
        """Setup the bishop route training interface"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("550x500")

        # Title
        tk.Label(self.root, text="Bishop Route Drill", font=("Arial", 18, "bold")).pack(pady=15)

        # Instructions
        tk.Label(self.root,
                 text="Find the connecting square(s) between each pair.\nThe bishop always needs exactly 2 moves per leg.",
                 font=("Arial", 11), fg="#555555", justify=tk.CENTER).pack(pady=(0, 10))

        # Route display
        self.route_frame = tk.Frame(self.root)
        self.route_frame.pack(pady=10)

        self.route_label = tk.Label(self.route_frame, text="", font=("Arial", 24, "bold"), fg="#333333")
        self.route_label.pack()

        # Answer area (hidden until Show Answer is pressed)
        self.answer_frame = tk.Frame(self.root)
        self.answer_frame.pack(pady=10, fill=tk.X, padx=30)

        self.answer_text = tk.Label(self.answer_frame, text="", font=("Arial", 14),
                                    fg="#1565C0", justify=tk.LEFT, wraplength=480)
        self.answer_text.pack()

        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        self.show_answer_btn = tk.Button(btn_frame, text="Show Answer", font=("Arial", 14),
                                         command=self.show_bishop_route_answer,
                                         bg="#2196F3", fg="black", width=14, height=2)
        self.show_answer_btn.pack(side=tk.LEFT, padx=10)

        self.next_route_btn = tk.Button(btn_frame, text="Next Route", font=("Arial", 14),
                                        command=self.show_new_bishop_route,
                                        bg="#4CAF50", fg="black", width=14, height=2)
        self.next_route_btn.pack(side=tk.LEFT, padx=10)

        # Back button
        back_btn = tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                             command=self.setup_start_screen,
                             bg="#9E9E9E", fg="black", width=14, height=1)
        back_btn.pack(pady=10)

    def show_new_bishop_route(self):
        """Generate and display a new bishop route"""
        self.current_route = self._generate_bishop_route()

        if self.current_route is None:
            self.route_label.config(text="Generation error — try again")
            return

        # Display route
        route_str = " → ".join(self.current_route)
        self.route_label.config(text=route_str)

        # Clear previous answer
        self.answer_text.config(text="")

        # Compute answers for each leg
        self.current_route_answers = []
        for i in range(len(self.current_route) - 1):
            sq_a = self.current_route[i]
            sq_b = self.current_route[i + 1]
            connecting = self._find_connecting_squares(sq_a, sq_b)
            self.current_route_answers.append((sq_a, sq_b, connecting))

    def show_bishop_route_answer(self):
        """Reveal the connecting squares for each leg"""
        if not hasattr(self, 'current_route_answers') or not self.current_route_answers:
            return

        lines = []
        for sq_a, sq_b, connecting in self.current_route_answers:
            if len(connecting) == 1:
                lines.append(f"{sq_a} → {sq_b}  :  {connecting[0]}")
            elif len(connecting) == 2:
                lines.append(f"{sq_a} → {sq_b}  :  {connecting[0]} or {connecting[1]}")
            else:
                lines.append(f"{sq_a} → {sq_b}  :  (none found)")

        self.answer_text.config(text="\n".join(lines))

    # ==================== KNIGHT ROUTE DRILL ====================

    def _knight_moves_from(self, f, r):
        """Return all squares reachable by a knight from (f, r)"""
        moves = []
        for df, dr in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]:
            nf, nr = f + df, r + dr
            if 0 <= nf <= 7 and 0 <= nr <= 7:
                moves.append((nf, nr))
        return moves

    def _find_knight_connecting_squares(self, sq_a, sq_b):
        """Find all intermediate squares for a knight moving from sq_a to sq_b in exactly 2 moves.

        An intermediate square must be reachable from sq_a in 1 knight move
        AND must reach sq_b in 1 knight move.
        """
        af, ar = self._sq_to_coords(sq_a)
        bf, br = self._sq_to_coords(sq_b)

        from_a = set(self._knight_moves_from(af, ar))
        from_b = set(self._knight_moves_from(bf, br))

        intermediates = from_a & from_b
        return sorted([self._coords_to_sq(f, r) for f, r in intermediates])

    def _build_knight_one_intermediate_lookup(self):
        """Build a lookup: for each square, which other squares are exactly 2 knight moves away
        with exactly 1 intermediate square?"""
        all_squares = [chr(f + ord('a')) + str(r + 1) for f in range(8) for r in range(8)]
        lookup = {}

        for sq in all_squares:
            af, ar = self._sq_to_coords(sq)
            from_a = set(self._knight_moves_from(af, ar))
            neighbors = []

            for sq2 in all_squares:
                if sq2 == sq:
                    continue
                bf, br = self._sq_to_coords(sq2)
                if (bf, br) in from_a:
                    continue  # Only 1 move away, skip

                from_b = set(self._knight_moves_from(bf, br))
                intermediates = from_a & from_b
                if len(intermediates) == 1:
                    neighbors.append(sq2)

            lookup[sq] = neighbors

        return lookup

    def _generate_knight_route(self):
        """Generate a route of 3 squares, no repeats,
        each consecutive pair exactly 2 knight moves apart with exactly 1 intermediate."""
        if not hasattr(self, '_knight_lookup'):
            self._knight_lookup = self._build_knight_one_intermediate_lookup()

        all_squares = [chr(f + ord('a')) + str(r + 1) for f in range(8) for r in range(8)]

        max_attempts = 200
        for _ in range(max_attempts):
            start = random.choice(all_squares)
            route = [start]

            success = True
            for step in range(2):
                candidates = [sq for sq in self._knight_lookup[route[-1]] if sq not in route]
                if not candidates:
                    success = False
                    break
                route.append(random.choice(candidates))

            if success and len(route) == 3:
                return route

        return None

    def setup_knight_route_screen(self):
        """Setup the knight route training interface"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("550x450")

        # Title
        tk.Label(self.root, text="Knight Route Drill", font=("Arial", 18, "bold")).pack(pady=15)

        # Instructions
        tk.Label(self.root,
                 text="Find the connecting square between each pair.\nThe knight always needs exactly 2 moves per leg (1 intermediate).",
                 font=("Arial", 11), fg="#555555", justify=tk.CENTER).pack(pady=(0, 10))

        # Route display
        self.route_frame = tk.Frame(self.root)
        self.route_frame.pack(pady=10)

        self.route_label = tk.Label(self.route_frame, text="", font=("Arial", 28, "bold"), fg="#333333")
        self.route_label.pack()

        # Answer area
        self.answer_frame = tk.Frame(self.root)
        self.answer_frame.pack(pady=10, fill=tk.X, padx=30)

        self.answer_text = tk.Label(self.answer_frame, text="", font=("Arial", 16),
                                    fg="#1565C0", justify=tk.LEFT, wraplength=480)
        self.answer_text.pack()

        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        self.show_answer_btn = tk.Button(btn_frame, text="Show Answer", font=("Arial", 14),
                                         command=self.show_knight_route_answer,
                                         bg="#2196F3", fg="black", width=14, height=2)
        self.show_answer_btn.pack(side=tk.LEFT, padx=10)

        self.next_route_btn = tk.Button(btn_frame, text="Next Route", font=("Arial", 14),
                                        command=self.show_new_knight_route,
                                        bg="#4CAF50", fg="black", width=14, height=2)
        self.next_route_btn.pack(side=tk.LEFT, padx=10)

        # Back button
        back_btn = tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                             command=self.setup_start_screen,
                             bg="#9E9E9E", fg="black", width=14, height=1)
        back_btn.pack(pady=10)

    def show_new_knight_route(self):
        """Generate and display a new knight route"""
        self.current_knight_route = self._generate_knight_route()

        if self.current_knight_route is None:
            self.route_label.config(text="Generation error — try again")
            return

        # Display route
        route_str = " → ".join(self.current_knight_route)
        self.route_label.config(text=route_str)

        # Clear previous answer
        self.answer_text.config(text="")

        # Compute answers for each leg
        self.current_knight_route_answers = []
        for i in range(len(self.current_knight_route) - 1):
            sq_a = self.current_knight_route[i]
            sq_b = self.current_knight_route[i + 1]
            connecting = self._find_knight_connecting_squares(sq_a, sq_b)
            self.current_knight_route_answers.append((sq_a, sq_b, connecting))

    def show_knight_route_answer(self):
        """Reveal the connecting squares for each leg in the format: a1 (c2) b3"""
        if not hasattr(self, 'current_knight_route_answers') or not self.current_knight_route_answers:
            return

        parts = []
        for i, (sq_a, sq_b, connecting) in enumerate(self.current_knight_route_answers):
            mid = connecting[0] if connecting else "?"
            if i == 0:
                parts.append(f"{sq_a} ({mid}) {sq_b}")
            else:
                parts.append(f"({mid}) {sq_b}")

        self.answer_text.config(text=" ".join(parts))

    # ==================== INTERSECTION DRILL ====================

    def _get_all_diagonals(self):
        """Return all diagonals on the board with 4+ squares as lists of (file, rank) coords."""
        diags = []

        # Anti-diagonals: f + r = k (goes from bottom-left to top-right)
        for k in range(1, 15):
            squares = []
            for f in range(8):
                r = k - f
                if 0 <= r <= 7:
                    squares.append((f, r))
            if len(squares) >= 4:
                diags.append(squares)

        # Main diagonals: f - r = k (goes from top-left to bottom-right)
        for k in range(-6, 7):
            squares = []
            for f in range(8):
                r = f - k
                if 0 <= r <= 7:
                    squares.append((f, r))
            if len(squares) >= 4:
                diags.append(squares)

        return diags

    def _diagonal_endpoints_label(self, squares):
        """Return a string like 'b8-h2' for a diagonal, with random endpoint order."""
        ep1 = self._coords_to_sq(*squares[0])
        ep2 = self._coords_to_sq(*squares[-1])
        if random.random() < 0.5:
            return f"{ep1}-{ep2}"
        else:
            return f"{ep2}-{ep1}"

    def _generate_intersection_question(self):
        """Generate one intersection question.

        Returns (question_text, answer_text) where answer is a square or 'no intersection'.
        Endpoint squares of the diagonal are excluded as answers to force real visualization.
        """
        if not hasattr(self, '_all_diagonals'):
            self._all_diagonals = self._get_all_diagonals()

        diag = random.choice(self._all_diagonals)
        diag_label = self._diagonal_endpoints_label(diag)

        # Interior squares only (exclude first and last)
        endpoints = {diag[0], diag[-1]}

        # Choose file or rank
        if random.random() < 0.5:
            # File question
            file_idx = random.randint(0, 7)
            file_name = chr(file_idx + ord('a'))
            question = f"{file_name}-file  and  diagonal {diag_label}"

            # Find intersection on interior squares only
            hit = None
            for f, r in diag:
                if f == file_idx and (f, r) not in endpoints:
                    hit = self._coords_to_sq(f, r)
                    break

            answer = hit if hit else "no intersection"
        else:
            # Rank question
            rank_idx = random.randint(0, 7)

            # Use ordinal for display
            ordinals = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th",
                        5: "5th", 6: "6th", 7: "7th", 8: "8th"}
            question = f"{ordinals[rank_idx + 1]} rank  and  diagonal {diag_label}"

            # Find intersection on interior squares only
            hit = None
            for f, r in diag:
                if r == rank_idx and (f, r) not in endpoints:
                    hit = self._coords_to_sq(f, r)
                    break

            answer = hit if hit else "no intersection"

        return question, answer

    def setup_intersection_screen(self):
        """Setup the intersection drill interface"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("600x550")

        # Title
        tk.Label(self.root, text="Intersection Drill", font=("Arial", 18, "bold")).pack(pady=15)

        # Instructions
        tk.Label(self.root,
                 text="Where do the file/rank and diagonal intersect?",
                 font=("Arial", 11), fg="#555555", justify=tk.CENTER).pack(pady=(0, 10))

        # Questions area
        self.questions_frame = tk.Frame(self.root)
        self.questions_frame.pack(pady=10, fill=tk.X, padx=30)

        self.question_labels = []
        self.answer_labels = []

        for i in range(5):
            row_frame = tk.Frame(self.questions_frame)
            row_frame.pack(fill=tk.X, pady=4)

            num_label = tk.Label(row_frame, text=f"{i+1}.", font=("Arial", 13, "bold"),
                                 width=3, anchor="e")
            num_label.pack(side=tk.LEFT)

            q_label = tk.Label(row_frame, text="", font=("Arial", 13), anchor="w")
            q_label.pack(side=tk.LEFT, padx=(5, 15))

            a_label = tk.Label(row_frame, text="", font=("Arial", 14, "bold"),
                               fg="#1565C0", anchor="w")
            a_label.pack(side=tk.LEFT)

            self.question_labels.append(q_label)
            self.answer_labels.append(a_label)

        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        self.show_answer_btn = tk.Button(btn_frame, text="Show Answer", font=("Arial", 14),
                                         command=self.show_intersection_answers,
                                         bg="#2196F3", fg="black", width=14, height=2)
        self.show_answer_btn.pack(side=tk.LEFT, padx=10)

        self.next_set_btn = tk.Button(btn_frame, text="Next 5", font=("Arial", 14),
                                      command=self.show_new_intersection_set,
                                      bg="#4CAF50", fg="black", width=14, height=2)
        self.next_set_btn.pack(side=tk.LEFT, padx=10)

        # Back button
        back_btn = tk.Button(self.root, text="← Back to Menu", font=("Arial", 11),
                             command=self.setup_start_screen,
                             bg="#9E9E9E", fg="black", width=14, height=1)
        back_btn.pack(pady=10)

    def show_new_intersection_set(self):
        """Generate and display 5 new intersection questions.
        At most 1 out of 5 (20%) may have 'no intersection' as the answer."""
        self.current_intersection_qa = []
        no_intersection_count = 0
        max_no_intersection = 1  # 20% of 5

        for i in range(5):
            # Keep generating until we get a valid question
            # (either has an intersection, or we haven't hit the no-intersection cap yet)
            max_retries = 50
            for _ in range(max_retries):
                question, answer = self._generate_intersection_question()
                if answer == "no intersection":
                    if no_intersection_count < max_no_intersection:
                        no_intersection_count += 1
                        break
                    # else: try again for one that has an intersection
                else:
                    break
            self.current_intersection_qa.append((question, answer))
            self.question_labels[i].config(text=question)
            self.answer_labels[i].config(text="")

    def show_intersection_answers(self):
        """Reveal all 5 answers"""
        if not hasattr(self, 'current_intersection_qa') or not self.current_intersection_qa:
            return

        for i, (question, answer) in enumerate(self.current_intersection_qa):
            self.answer_labels[i].config(text=f"→  {answer}")

    # ==================== COMMON METHODS ====================

    def abort_training(self):
        """Abort the current training session and return to menu"""
        self.training_active = False
        self.setup_start_screen()

    def check_time(self):
        """Check if training time has elapsed"""
        if not self.training_active:
            return

        elapsed = time.time() - self.start_time
        remaining = self.duration_seconds - elapsed

        # Update time display
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        self.time_label.config(text=f"Time remaining: {minutes:02d}:{seconds:02d}")

        if remaining <= 0:
            self.end_training()
        else:
            # Check again in 1 second
            self.root.after(1000, self.check_time)

    def end_training(self):
        """End the training session and show results"""
        self.training_active = False

        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("400x300")

        # Results screen
        tk.Label(self.root, text="Training Complete!", font=("Arial", 24, "bold"),
                 fg="#4CAF50").pack(pady=30)

        # Only show streak for square color drill
        if self.drill_type == "square_color":
            tk.Label(self.root, text=f"Highest Correct Streak:", font=("Arial", 14)).pack(pady=5)
            tk.Label(self.root, text=str(self.highest_streak), font=("Arial", 36, "bold"),
                     fg="#2196F3").pack(pady=10)

        # Restart button
        restart_btn = tk.Button(self.root, text="New Session", font=("Arial", 14),
                                command=self.setup_start_screen, bg="#2196F3", fg="black",
                                padx=20, pady=10)
        restart_btn.pack(pady=30)


def main():
    root = tk.Tk()
    app = ChessTrainer(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox
import random
import time


class ChessTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Trainer")
        self.root.geometry("500x550")
        
        # Training state
        self.training_active = False
        self.current_streak = 0
        self.highest_streak = 0
        self.start_time = None
        self.duration_seconds = 0
        self.drill_type = None
        
        # Setup UI
        self.setup_start_screen()
    
    def setup_start_screen(self):
        """Initial screen to set duration and start training"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("500x550")
        
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
    
    def start_training(self, drill_type):
        """Begin the training session"""
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
        
        self.check_time()
    
    # ==================== SQUARE COLOR DRILL ====================
    
    def setup_square_color_screen(self):
        """Setup the square color training interface"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("400x350")
        
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
        
        # Time remaining label
        self.time_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.time_label.pack(pady=5)
    
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
        
        # Time remaining label
        self.time_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.time_label.pack(pady=5)
    
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
        
        # Generate target square (same color as bishop, different from queen and bishop)
        while True:
            target_file = random.choice(files)
            target_rank = random.choice(ranks)
            target_square = target_file + target_rank
            target_color = self.get_square_color_numeric(target_square)
            
            if (target_square != queen_square and 
                target_square != bishop_square and 
                target_color == bishop_color):
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
        
        # Time remaining label
        self.time_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.time_label.pack(pady=5)
    
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
        
        # Time remaining label
        self.time_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.time_label.pack(pady=5)
    
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
        
        # Time remaining label
        self.time_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.time_label.pack(pady=5)
    
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
    
    # ==================== COMMON METHODS ====================
    
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

import customtkinter as ctk
import google.generativeai as genai
from datetime import datetime
import json
import asyncio
import pandas as pd
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
import re

class LotteryPredictor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Lottery Prediction Assistant")
        self.geometry("1400x900")
        ctk.set_appearance_mode("dark")
        
        # Define colors
        self.colors = {
            "bg_dark": "#1a1a1a",
            "bg_light": "#2d2d2d",
            "text_primary": "#ffffff",
            "text_secondary": "#b3b3b3",
            "accent": "#007AFF",
            "user_msg_bg": "#264F78",
            "assistant_msg_bg": "#2D3748",
            "system_msg_bg": "#7B341E"
        }
        
        # Initialize Gemini API
        self.api_key = "AIzaSyAKlVjMgHm0ArJqQiWNmXHnYr-ZPKL88CI"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Initialize chat history
        self.chat_history = []
        self.current_chat = None
        
        # Initialize thread pool
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        # Lottery assistant prompt
        self.assistant_prompt = """You are a lottery prediction assistant with expertise in statistical analysis and pattern recognition. Analyze lottery data and provide insights using:
        1. Statistical pattern analysis
        2. Historical data correlation
        3. Numerical sequence analysis
        4. Probability calculations
        Provide detailed explanations of your analysis and recommendations."""
        
        self.create_gui()
        self.create_new_chat()
        
    def create_gui(self):
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left sidebar
        self.left_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_dark"])
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(10,5), pady=10)
        
        # Main chat area
        self.right_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_light"])
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=10)
        
        self.create_left_sidebar()
        self.create_chat_interface()
        
    def create_left_sidebar(self):
        # Title
        title_label = ctk.CTkLabel(
            self.left_frame,
            text="Lottery Assistant",
            font=("TkDefaultFont", 24),
            text_color=self.colors["text_primary"]
        )
        title_label.pack(pady=(20,30), padx=20)
        
        # New Chat Button
        new_chat_btn = ctk.CTkButton(
            self.left_frame,
            text="New Chat",
            font=("TkDefaultFont", 16),
            height=40,
            command=self.create_new_chat,
            fg_color=self.colors["accent"]
        )
        new_chat_btn.pack(pady=(0,20), padx=20, fill="x")
        
        # Chat History
        history_label = ctk.CTkLabel(
            self.left_frame,
            text="Chat History",
            font=("TkDefaultFont", 18),
            text_color=self.colors["text_secondary"]
        )
        history_label.pack(pady=(0,10), padx=20)
        
        self.history_list = ctk.CTkScrollableFrame(
            self.left_frame,
            fg_color=self.colors["bg_dark"]
        )
        self.history_list.pack(fill="both", expand=True, padx=10, pady=(0,10))
        
    def create_chat_interface(self):
        # Chat display
        self.chat_display = ctk.CTkTextbox(
            self.right_frame,
            wrap="word",
            font=("TkDefaultFont", 16),
            fg_color=self.colors["bg_light"]
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=(20,10))
        
        # Input area
        self.input_frame = ctk.CTkFrame(self.right_frame, fg_color=self.colors["bg_light"])
        self.input_frame.pack(fill="x", padx=20, pady=(10,20))
        
        self.message_input = ctk.CTkTextbox(
            self.input_frame,
            height=100,
            wrap="word",
            font=("TkDefaultFont", 16),
            fg_color=self.colors["bg_dark"]
        )
        self.message_input.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=100,
            height=40,
            font=("TkDefaultFont", 16),
            command=self.handle_send_message,
            fg_color=self.colors["accent"]
        )
        self.send_button.pack(side="right")

    def create_new_chat(self):
        new_chat = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'title': "New Conversation",
            'messages': []
        }
        self.chat_history.insert(0, new_chat)
        self.current_chat = new_chat
        self.update_chat_history_display()
        self.clear_chat_display()

    def update_chat_history_display(self):
        for widget in self.history_list.winfo_children():
            widget.destroy()
            
        for chat in self.chat_history:
            btn = ctk.CTkButton(
                self.history_list,
                text=chat['title'],
                font=("TkDefaultFont", 14),
                height=35,
                command=lambda c=chat: self.load_chat(c)
            )
            btn.pack(fill="x", pady=2)

    def load_chat(self, chat):
        self.current_chat = chat
        self.clear_chat_display()
        for message in chat['messages']:
            self.display_message(message['role'], message['content'])

    def clear_chat_display(self):
        self.chat_display.delete("1.0", "end")

    def handle_send_message(self):
        content = self.message_input.get("1.0", "end-1c").strip()
        if not content:
            return
            
        self.message_input.delete("1.0", "end")
        self.display_message("user", content)
        threading.Thread(target=self.run_async_send_message, args=(content,)).start()

    def run_async_send_message(self, content):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.process_message(content))
        finally:
            loop.close()

    async def process_message(self, content):
        if not self.current_chat:
            self.create_new_chat()
            
        full_prompt = f"{self.assistant_prompt}\n\nUser: {content}"
        
        try:
            # Send to Gemini API and get full response
            response = await self.send_to_gemini(full_prompt)
            
            # Add extra newline at the end
            self.after(0, lambda: self.chat_display.insert("end", "\n"))
            
            # Update chat history
            self.after(0, lambda: self.handle_api_response(content, response))
            
        except Exception as e:
            self.after(0, lambda: self.display_message("system", f"Error: {str(e)}"))

    def handle_api_response(self, content, response):
        """Update chat history after response is complete"""
        self.current_chat['messages'].extend([
            {'role': 'user', 'content': content},
            {'role': 'assistant', 'content': response}
        ])
        
        if len(self.current_chat['messages']) == 2:
            self.current_chat['title'] = content[:30] + ("..." if len(content) > 30 else "")
            self.update_chat_history_display()

    async def send_to_gemini(self, prompt):
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,
                    top_k=1,
                    top_p=1,
                    max_output_tokens=2048,
                ),
                stream=True  # Enable streaming
            )
            
            # Initialize variables for streaming
            full_response = ""
            timestamp = datetime.now().strftime("%H:%M")
            
            # Add assistant header first
            self.after(0, lambda: self.start_assistant_message(timestamp))
            
            # Process the stream
            async for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    # Update display with new chunk
                    self.after(0, lambda text=chunk.text: self.update_streaming_message(text, timestamp))
            
            return full_response
            
        except Exception as e:
            print(f"API Error details: {str(e)}")
            raise Exception(f"Error generating content: {str(e)}")

    def update_streaming_message(self, new_text, timestamp):
        """Update the display with new chunks of text"""
        # Insert new text
        self.chat_display.insert("end", new_text)
        
        # Update bubble
        self.chat_display.tag_add(
            f"bubble_{timestamp}",
            self.current_message_start,
            "end-1c"
        )
        
        # Add extra newline if it's the end of a sentence
        if new_text.strip().endswith((".", "!", "?")):
            self.chat_display.insert("end", "\n")
        
        # Scroll to show new text
        self.chat_display.see("end")


    def start_assistant_message(self, timestamp):
        """Initialize the assistant message display"""
        self.chat_display.tag_config("timestamp", foreground=self.colors["text_secondary"])
        self.chat_display.tag_config("role_assistant", foreground="#00CF7F")
        
        self.chat_display.insert("end", f"\n[{timestamp}] ", "timestamp")
        self.chat_display.insert("end", "Assistant:", "role_assistant")
        self.chat_display.insert("end", "\n")
        
        # Store the starting position for the bubble
        self.current_message_start = self.chat_display.index("end-1c")
        
        # Configure the bubble tag
        self.chat_display.tag_config(
            f"bubble_{timestamp}",
            background=self.colors["assistant_msg_bg"],
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
            spacing1=10,
            spacing3=10
        )
        
        self.chat_display.see("end")

    def format_message_text(self, text):
        formatted_text = text
        formatted_text = re.sub(r'\*\*(.*?)\*\*', r'\1', formatted_text)  # Remove markdown
        formatted_text = re.sub(r'^\* ', '• ', formatted_text, flags=re.MULTILINE)
        formatted_text = re.sub(r'^\d+\. ', lambda m: f'{m.group()}'.ljust(4), formatted_text, flags=re.MULTILINE)
        return formatted_text

    def display_message(self, role, content):
        timestamp = datetime.now().strftime("%H:%M")
        formatted_content = self.format_message_text(content)
        
        # Configure tags for colors only (no fonts)
        self.chat_display.tag_config("timestamp", foreground=self.colors["text_secondary"])
        self.chat_display.tag_config("role_user", foreground=self.colors["accent"])
        self.chat_display.tag_config("role_assistant", foreground="#00CF7F")
        self.chat_display.tag_config("role_system", foreground="#FF6B6B")
        
        # Insert message with role-specific colors
        self.chat_display.insert("end", f"\n[{timestamp}] ", "timestamp")
        
        if role == "user":
            self.chat_display.insert("end", "You:", "role_user")
            msg_bg = self.colors["user_msg_bg"]
        elif role == "assistant":
            self.chat_display.insert("end", "Assistant:", "role_assistant")
            msg_bg = self.colors["assistant_msg_bg"]
        else:
            self.chat_display.insert("end", "System:", "role_system")
            msg_bg = self.colors["system_msg_bg"]
        
        # Insert content with background
        self.chat_display.insert("end", "\n")
        content_start = self.chat_display.index("end-1c")
        self.chat_display.insert("end", f"{formatted_content}\n\n")
        
        # Apply background color
        self.chat_display.tag_add(
            f"bubble_{timestamp}",
            content_start,
            "end-1c"
        )
        self.chat_display.tag_config(
            f"bubble_{timestamp}",
            background=msg_bg,
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
            spacing1=10,
            spacing3=10
        )
        
        self.chat_display.see("end")

if __name__ == "__main__":
    app = LotteryPredictor()
    app.mainloop()

from nicegui import ui
from openai import AzureOpenAI
from dotenv import load_dotenv
from os import getenv
from typing import Optional

# Load environment variables
load_dotenv()

class OpenAIStreamer:
    def __init__(self):
        self.is_streaming = False
        self.textarea: Optional[ui.textarea] = None
        self.client = AzureOpenAI(
            api_key=getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=getenv("AZURE_OPENAI_API_VERSION")
        )
        self.MODEL_NAME = "gpt-4o"
        self.prompt = """
        Generate XML content for the given query. Example:
        <root>
          <tag1>value1</tag1>
          <tag2>value2</tag2>
          <tag3>value3</tag3>
        </root>
        Ensure the output is valid XML, with properly closed tags and no extraneous content.
        Provide the content for tag1, tag2, and tag3 based on the user's input context.
        Do not include markdown code blocks or backticks.
        """

    def generate_xml(self, user_input: str):
        self.textarea.value = ""  # Clear previous content
        
        stream = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates valid XML according to the provided schema."},
                {"role": "user", "content": self.prompt},
                {"role": "user", "content": user_input}
            ],
            stream=True
        )

        xml_output = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta:
                data = chunk.choices[0].delta
                if data and hasattr(data, "content"):
                    content = data.content
                    if content is None:
                        continue
                    xml_output += content
                    self.textarea.value = xml_output
                    ui.update(self.textarea)  # Force UI update
        
        stream.close()

    def toggle_streaming(self, user_input):
        self.is_streaming = not self.is_streaming
        if self.is_streaming:
            if not user_input.value:
                ui.notify("Please enter some text first", type="negative")
                self.is_streaming = False
                return
            
            ui.notify("Starting XML generation with OpenAI...")
            self.generate_xml(user_input.value)
        else:
            ui.notify("Stopped XML generation")

# Create the streamer instance
streamer = OpenAIStreamer()

# Create UI
with ui.card().classes("w-full max-w-2xl mx-auto"):
    ui.label("OpenAI XML Stream Generator").classes("text-2xl")
    
    # Input section
    with ui.row().classes("w-full items-end"):
        user_input = ui.input(
            label="Enter your context", 
            placeholder="e.g., 'Poodle dog age 3 healthy'",
        ).classes("flex-grow")
        
        ui.button("Clear", on_click=lambda: user_input.set_value("")).props("outline")
    
    # Text output area
    streamer.textarea = ui.textarea(label="Generated XML") \
        .props("readonly autogrow") \
        .classes("w-full font-mono")
    
    # Control buttons
    with ui.row().classes("w-full"):
        ui.button("Toggle Generation", 
                 on_click=lambda: streamer.toggle_streaming(user_input)) \
            .classes("flex-grow") \
            .props("color=primary")
        
        ui.button("Clear Output", 
                 on_click=lambda: streamer.textarea.set_value("")) \
            .props("outline") \
            .classes("flex-grow")

ui.run()
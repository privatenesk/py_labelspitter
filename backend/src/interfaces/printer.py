from abc import ABC, abstractmethod
from PIL import Image
import os
import time

class PrinterInterface(ABC):
    @abstractmethod
    def print_image(self, image: Image.Image):
        """Prints the given PIL Image."""
        pass

class MockPrinter(PrinterInterface):
    def __init__(self, output_dir: str = "printer_output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def print_image(self, image: Image.Image):
        timestamp = int(time.time())
        filename = f"{self.output_dir}/label_{timestamp}.png"
        image.save(filename)
        print(f"[MockPrinter] Saved label to {filename} (Size: {image.size})")

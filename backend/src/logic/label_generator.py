from PIL import Image, ImageDraw, ImageFont
import math
from backend.src.core.config import settings

class LabelGenerator:
    def __init__(self):
        self.dpi = settings.PRINTER_DPI
        self.width_mm = settings.PRINTER_WIDTH_MM
        self.px_per_mm = self.dpi / 25.4
        self.width_px = int(self.width_mm * self.px_per_mm)

    def _mm_to_px(self, mm):
        return int(mm * self.px_per_mm)

    def generate(self, title: str, category: str, difficulty: int, options: dict = None) -> Image.Image:
        # Calculate height
        # Base height 30mm for difficulty 1, + 15mm per extra difficulty level
        # Max (diff 5) = 90mm
        # Clamping difficulty 1-10 just in case
        difficulty = max(1, min(10, difficulty))

        height_mm = 30 + (difficulty - 1) * 15
        height_px = self._mm_to_px(height_mm)

        # Create image (White background)
        # mode '1' (1-bit pixels, black and white) is standard for thermal printers,
        # but we draw in 'L' (grayscale) or 'RGB' then convert to '1' with dither if needed.
        # Brother QL-800 driver usually accepts RGB/Greyscale.
        image = Image.new('RGB', (self.width_px, height_px), 'white')
        draw = ImageDraw.Draw(image)

        # Draw Fillers (Top and Bottom)
        self._draw_fillers(draw, 0, self.width_px, self._mm_to_px(10), "top")
        self._draw_fillers(draw, height_px - self._mm_to_px(10), self.width_px, height_px, "bottom")

        # Draw Text
        # Fonts
        try:
            # Try to use a larger default font
            title_font_size = 40
            cat_font_size = 24
            title_font = ImageFont.load_default(size=title_font_size)
            cat_font = ImageFont.load_default(size=cat_font_size)
        except Exception:
            # Fallback for older pillow if strict dep (though we checked 12.1.0)
            title_font = ImageFont.load_default()
            cat_font = ImageFont.load_default()

        # Center Text
        # Title
        # textbbox returns (left, top, right, bottom)
        _, _, w_title, h_title = draw.textbbox((0, 0), title, font=title_font)
        x_title = (self.width_px - w_title) / 2

        # Category
        _, _, w_cat, h_cat = draw.textbbox((0, 0), category, font=cat_font)
        x_cat = (self.width_px - w_cat) / 2

        # Vertical Positioning: Center in the middle area (between fillers)
        top_filler_h = self._mm_to_px(10)
        bottom_filler_start = height_px - self._mm_to_px(10)
        available_h = bottom_filler_start - top_filler_h

        center_y = top_filler_h + (available_h / 2)

        # Draw Title slightly above center, Category below
        draw.text((x_title, center_y - h_title - 5), title, font=title_font, fill='black')
        draw.text((x_cat, center_y + 10), category.upper(), font=cat_font, fill='black')

        return image

    def _draw_fillers(self, draw, y_start, width, y_end, position):
        # simple hatched pattern
        step = 20
        for i in range(0, width + (y_end - y_start), step):
            start = (i, y_start)
            end = (i - (y_end - y_start), y_end)
            draw.line([start, end], fill='black', width=2)

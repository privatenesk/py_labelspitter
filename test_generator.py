import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from backend.src.logic.label_generator import LabelGenerator

def test_generation():
    generator = LabelGenerator()

    # Test Difficulty 1
    print("Generating Difficulty 1 Label...")
    img1 = generator.generate("Small Task", "Quick", 1)
    img1.save("test_label_diff1.png")
    print(f"Saved test_label_diff1.png: {img1.size}")

    # Test Difficulty 5
    print("Generating Difficulty 5 Label...")
    img5 = generator.generate("Huge Project", "Deep Work", 5)
    img5.save("test_label_diff5.png")
    print(f"Saved test_label_diff5.png: {img5.size}")

    # Verify Sizes
    # Diff 1: 30mm -> ~30 * 11.8 = 354 px
    # Diff 5: 90mm -> ~90 * 11.8 = 1062 px
    assert img1.size[1] < img5.size[1]
    print("Verification Successful: Difficulty affects height.")

if __name__ == "__main__":
    test_generation()

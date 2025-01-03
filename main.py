import random
import argparse

from openai import OpenAI


OPENAI_API_SECRET = ''

OPENAI_CLIENT = OpenAI(api_key=OPENAI_API_SECRET)


def generate_fuzzy_text(prompt, variations=1):
    prompt = ('Generate a complex string up to 100 characters long that includes a mix of various languages '
              'right to left, left to right, symbols and anything that can crash target app which expected user input '
              'to test the robustness of software systems. Include characters from Arabic, Chinese, Hebrew, and embed '
              'special symbols like section signs, copyright, and trademark symbols. The string should be challenging '
              'and used to identify potential crashes in systems, particularly those running on platforms like '
              f' {prompt}. Focus on diverse and intricate characters combinations. generate {variations} variations '
              f'and provide only fuzzy string no any extra text or anything just list ov {variations} examples')

    print("Request to ChatGPT...")
    response = OPENAI_CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    response = response.choices[0].message.content.strip()
    return response


def enhance_string_complexity(original_string, size):
    special_chars = ['\0', '\b', '\t', '\n', '\r', '\f', '\v', '©', '®', '±', '§', '¥', '€', '₹', '£', '¢']
    # Unicode ranges for Arabic, Chinese, Hebrew, special symbols
    unicode_ranges = [
        (0x0600, 0x06FF),  # Arabic
        (0x4E00, 0x9FFF),  # Chinese
        (0x0590, 0x05FF),  # Hebrew
        (0x00A1, 0x00AC),  # Special symbols like section sign
        (0x00AE, 0x00FF)  # More special symbols
    ]

    characters = list(original_string)
    max_iterations = size - len(characters)
    for _ in range(max_iterations):
        if random.choice([True, False]):
            if characters:  # Ensure there's at least one character to multiply
                char_to_multiply = random.choice(characters)
                repetitions = random.randint(1, 3)
                characters.append(char_to_multiply * repetitions)
        else:
            if random.choice([True, False]):  # Choose between special_chars and unicode ranges
                characters.append(random.choice(special_chars))
            else:
                range_choice = random.choice(unicode_ranges)
                characters.append(chr(random.randint(range_choice[0], range_choice[1])))

        if len(''.join(characters)) >= size:
            break

    return ''.join(characters)


def decorate_and_save_responses(response, variations, size, filename="output.txt"):
    print("Decoration in process...")
    with open(filename, 'w', encoding='utf-8') as file:
        for i in range(variations):
            file.write(f"{enhance_string_complexity(response, size)}\n")
    print("Done")


def main():
    print("Welcome to FuzzNova - Your Fuzz Testing Assistant")
    parser = argparse.ArgumentParser(description="FuzzNova is generate and decorate sequence of symbols for fuzz testing.")
    parser.add_argument('-o', '--output', default='output.txt', help='Output file name (default: output.txt)')
    parser.add_argument('-v', '--variations', type=int, default=10, help='Number of variations requested (default: 1)')
    parser.add_argument('-s', '--size', type=int, default=999, help='Max size of decoration each variation (default: 999)')
    parser.add_argument('-t', '--target', required=True, help='Target description Example "C++, GCC, Linux"')

    args = parser.parse_args()
    responses = generate_fuzzy_text(args.target, args.variations)
    decorate_and_save_responses(responses, args.variations, args.size, args.output)

    print(f"Generated result have been saved to '{args.output}'.")


if __name__ == "__main__":
    main()

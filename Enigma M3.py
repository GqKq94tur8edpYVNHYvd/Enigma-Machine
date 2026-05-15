class Enigma:
    def __init__(self, rotor_choices, ring_settings,
                 initial_positions, reflector_choice,
                 plugboard_settings):

        # Rotor wirings
        rotor_wirings = [
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # I
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # II
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # III
            "ESOVPZJAYQUIRHXLNFTGKDCMWB",  # IV
            "VZBRGITYUPSDNHLXAWMJQOFECK",  # V
            "JPGVOUMFYQBENHZRDKASXLICTW",  # VI
            "NZJHGRCXMYSWBOUFAIVLPEKQDT",  # VII
            "FKQHTLXOCBJSPDZRAMEWNIUYGV"   # VIII
        ]

        rotor_labels = ['I', 'II', 'III', 'IV',
                        'V', 'VI', 'VII', 'VIII']

        rotor_index_map = {
            label: index for index, label in enumerate(rotor_labels)
        }

        rotor_index_map.update({
            label.lower(): index
            for label, index in rotor_index_map.items()
        })

        # Turnover notches
        turnover_notches = [
            [16],      # I   Q
            [4],       # II  E
            [21],      # III V
            [9],       # IV  J
            [25],      # V   Z
            [12, 25],  # VI  M,Z
            [12, 25],  # VII M,Z
            [12, 25]   # VIII M,Z
        ]

        # Reflectors
        reflectors = {
            'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }

        # ---------------- VALIDATION ----------------

        if len(rotor_choices) != 3:
            raise ValueError("Exactly 3 rotors are required.")

        if len(set(choice.upper() for choice in rotor_choices)) != 3:
            raise ValueError("Rotors must be unique.")

        if len(ring_settings) != 3:
            raise ValueError("Ring settings must contain 3 letters.")

        if len(initial_positions) != 3:
            raise ValueError("Initial positions must contain 3 letters.")

        reflector_choice = reflector_choice.upper()

        if reflector_choice not in reflectors:
            raise ValueError("Reflector must be B or C.")

        if len(plugboard_settings) > 10:
            raise ValueError("Maximum 10 plugboard pairs allowed.")

        used_letters = set()

        for pair in plugboard_settings:

            if len(pair) != 2 or not pair.isalpha():
                raise ValueError(f"Invalid plugboard pair: {pair}")

            a, b = pair[0].upper(), pair[1].upper()

            if a == b:
                raise ValueError(f"Invalid plugboard pair: {pair}")

            if a in used_letters or b in used_letters:
                raise ValueError(
                    f"Plugboard letter reused: {pair}"
                )

            used_letters.add(a)
            used_letters.add(b)

        # ---------------- ROTOR SETUP ----------------

        chosen_rotors = [
            rotor_index_map[choice]
            for choice in rotor_choices
        ]

        self.rotors = [
            [ord(c) - ord('A') for c in rotor_wirings[i]]
            for i in chosen_rotors
        ]

        self.inverse_rotors = []

        for rotor in self.rotors:
            inverse = [0] * 26

            for i, value in enumerate(rotor):
                inverse[value] = i

            self.inverse_rotors.append(inverse)

        self.turnovers = [
            turnover_notches[i]
            for i in chosen_rotors
        ]

        self.reflector = [
            ord(c) - ord('A')
            for c in reflectors[reflector_choice]
        ]

        self.ring_settings = [
            ord(c.upper()) - ord('A')
            for c in ring_settings
        ]

        self.positions = [
            ord(c.upper()) - ord('A')
            for c in initial_positions
        ]

        # ---------------- PLUGBOARD ----------------

        self.plugboard = {i: i for i in range(26)}

        for pair in plugboard_settings:

            a = ord(pair[0].upper()) - ord('A')
            b = ord(pair[1].upper()) - ord('A')

            self.plugboard[a] = b
            self.plugboard[b] = a

    # -------------------------------------------------

    def rotate(self):

        left_at_notch = (
            self.positions[1] in self.turnovers[1]
        )

        right_at_notch = (
            self.positions[2] in self.turnovers[2]
        )

        # Double-step behavior

        if left_at_notch:
            self.positions[0] = (
                self.positions[0] + 1
            ) % 26

            self.positions[1] = (
                self.positions[1] + 1
            ) % 26

        elif right_at_notch:
            self.positions[1] = (
                self.positions[1] + 1
            ) % 26

        # Right rotor always rotates

        self.positions[2] = (
            self.positions[2] + 1
        ) % 26

    # -------------------------------------------------

    def encode_char(self, char):

        if not char.isalpha():
            return ''

        char = char.upper()

        # Rotate FIRST (historically correct)

        self.rotate()

        # Plugboard in

        char_index = self.plugboard[
            ord(char) - ord('A')
        ]

        # Forward through rotors
        # Right -> Left

        for i in range(2, -1, -1):

            offset = (
                char_index
                + self.positions[i]
                - self.ring_settings[i]
            ) % 26

            char_index = (
                self.rotors[i][offset]
                - self.positions[i]
                + self.ring_settings[i]
            ) % 26

        # Reflector

        char_index = self.reflector[char_index]

        # Backward through rotors
        # Left -> Right

        for i in range(3):

            offset = (
                char_index
                + self.positions[i]
                - self.ring_settings[i]
            ) % 26

            char_index = (
                self.inverse_rotors[i][offset]
                - self.positions[i]
                + self.ring_settings[i]
            ) % 26

        # Plugboard out

        char_index = self.plugboard[char_index]

        return chr(char_index + ord('A'))

    # -------------------------------------------------

    def encode(self, message):

        encoded = ''.join(
            self.encode_char(c)
            for c in message
            if c.isalpha()
        )

        # Group into blocks of 5

        groups = [
            encoded[i:i + 4]
            for i in range(0, len(encoded), 4)
        ]

        formatted = '\n'.join(
            ' '.join(groups[i:i + 10])
            for i in range(0, len(groups), 10)
                )

        return formatted


# =====================================================

def setup_enigma():

    print("\n=== ENIGMA M3 SIMULATOR ===\n")

    reflector_choice = input(
        "Choose reflector (B or C): "
    ).strip()

    rotor_choices = input(
        "Enter 3 rotors "
        "(example: IV III II): "
    ).split()

    ring_settings = input(
        "Enter ring settings "
        "(example: AAA): "
    ).strip()

    initial_positions = input(
        "Enter initial positions "
        "(example: AAA): "
    ).strip()

    plugboard_input = input(
        "Enter up to 10 plugboard pairs "
        "(example: AB CD EF)\n"
        "or NONE for no plugboard:\n"
    ).strip()

    if plugboard_input.lower() == 'none':
        plugboard_settings = []
    else:
        plugboard_settings = plugboard_input.split()

    enigma_machine = Enigma(
        rotor_choices,
        ring_settings,
        initial_positions,
        reflector_choice,
        plugboard_settings
    )

    print(
        "\nEnter plaintext message "
        "(finish with an empty line):"
    )

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    plaintext = '\n'.join(lines)

    encoded_message = enigma_machine.encode(
        plaintext
    )

    print("\nEncoded message:\n")
    print(encoded_message)


# =====================================================

if __name__ == "__main__":
    setup_enigma()

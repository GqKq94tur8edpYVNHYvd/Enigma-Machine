class Enigma:
    def __init__(self, rotor_choices, ring_settings, initial_positions, reflector_choice, plugboard_settings):
        rotor_wirings = [
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # Rotor III
            "ESOVPZJAYQUIRHXLNFTGKDCMWB",  # Rotor IV
            "VZBRGITYUPSDNHLXAWMJQOFECK"   # Rotor V
        ]
        rotor_labels = ['I', 'II', 'III', 'IV', 'V']
        rotor_index_map = {label: index for index, label in enumerate(rotor_labels)}
        rotor_index_map.update({label.lower(): index for label, index in rotor_index_map.items()})

        turnover_notches = [
            [16],  # Rotor I   (Q -> R)
            [4],   # Rotor II  (E -> F)
            [21],  # Rotor III (V -> W)
            [9],   # Rotor IV  (J -> K)
            [25]   # Rotor V   (Z -> A)
        ]

        reflectors = {
            'A': "EJMZALYXVBWFCRQUONTSPIKHGD",  # Reflector A
            'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",  # Reflector B
            'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"   # Reflector C
        }

        self.etw = list(range(26))  # Entry Wheel

        chosen_rotors = [rotor_index_map[choice] for choice in rotor_choices]
        self.rotors = [[ord(c) - ord('A') for c in rotor_wirings[i]] for i in chosen_rotors]
        self.turnovers = [turnover_notches[i] for i in chosen_rotors]
        self.reflector = [ord(c) - ord('A') for c in reflectors[reflector_choice.upper()]]
        self.ring_settings = [ord(c.upper()) - ord('A') for c in ring_settings]
        self.positions = [ord(c.upper()) - ord('A') for c in initial_positions]

        self.plugboard = {i: i for i in range(26)}
        for pair in plugboard_settings:
            if pair:
                a, b = ord(pair[0].upper()) - ord('A'), ord(pair[1].upper()) - ord('A')
                self.plugboard[a], self.plugboard[b] = b, a

    def rotate(self):
        carry = True
        for i in range(2, -1, -1):
            if carry:
                carry = self.positions[i] in self.turnovers[i]
                self.positions[i] = (self.positions[i] + 1) % 26

    def encode_char(self, char):
        char_index = self.plugboard[ord(char) - ord('A')]

        self.rotate()

        for i in range(2, -1, -1):
            char_index = (self.rotors[i][(char_index + self.positions[i] - self.ring_settings[i]) % 26] -
                          self.positions[i] + self.ring_settings[i]) % 26

        char_index = self.reflector[char_index]

        for i in range(3):
            char_index = (self.rotors[i].index((char_index + self.positions[i] - self.ring_settings[i]) % 26) -
                          self.positions[i] + self.ring_settings[i]) % 26

        return chr(self.plugboard[char_index] + ord('A'))

    def encode(self, message):
        encoded = ''.join(self.encode_char(c) for c in message.upper() if c.isalpha())
        groups = [' '.join([encoded[i:i + 5] for i in range(0, len(encoded), 5)][j:j + 5]) for j in
                  range(0, len(encoded) // 5, 5)]
        return '\n'.join(groups)


def setup_enigma():
    def get_input(prompt, valid_choices=None, transform=str, validation=None):
        while True:
            user_input = input(prompt).strip()
            if valid_choices and user_input.upper() not in valid_choices:
                print(f"Invalid choice. Choose from {valid_choices}.")
                continue
            if validation and not validation(user_input):
                print("Invalid input.")
                continue
            return transform(user_input)

    reflector_choice = get_input("Choose reflector (A, B, or C): ", valid_choices={'A', 'B', 'C'}, transform=str.upper)
    rotor_choices = get_input("Enter rotor choices (e.g., IV III II or iv iii ii): ", transform=lambda s: s.split())
    ring_settings = get_input("Enter ring settings without spaces (e.g., AAA or aaa): ")
    initial_positions = get_input("Enter initial positions without spaces (e.g., AAA or aaa): ")
    plugboard_pairs = get_input(
        "Enter up to 10 plugboard pairs separated by space (e.g., AB CD EF or ab cd ef or none for no pairs): ",
        transform=lambda s: [] if s.lower() == 'none' else s.split()
    )

    enigma_machine = Enigma(rotor_choices, ring_settings, initial_positions, reflector_choice, plugboard_pairs)
    plaintext = get_input("Enter the plaintext message to encode: ")
    encoded_message = enigma_machine.encode(plaintext)
    print("Encoded message:")
    print(encoded_message)


setup_enigma()

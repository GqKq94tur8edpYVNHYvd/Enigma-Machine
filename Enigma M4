class Enigma:
    def __init__(self, rotor_choices, ring_settings, initial_positions, reflector_choice, plugboard_settings):
        rotor_wirings = [
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # Rotor III
            "ESOVPZJAYQUIRHXLNFTGKDCMWB",  # Rotor IV
            "VZBRGITYUPSDNHLXAWMJQOFECK",  # Rotor V
            "JPGVOUMFYQBENHZRDKASXLICTW",  # Rotor VI
            "NZJHGRCXMYSWBOUFAIVLPEKQDT",  # Rotor VII
            "FKQHTLXOCBJSPDZRAMEWNIUYGV",  # Rotor VIII
            "LEYJVCNIXWPBQMDRTAKZGFUHOS",  # Rotor IX (Beta)
            "FSOKANUERHMBTIYCWLQPZXVGJD"   # Rotor X (Gamma)
        ]
        rotor_labels = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
        rotor_index_map = {label: index for index, label in enumerate(rotor_labels)}

        turnover_notches = [
            [16],     # Rotor I (Q)
            [4],      # Rotor II (E)
            [21],     # Rotor III (V)
            [9],      # Rotor IV (J)
            [25],     # Rotor V (Z)
            [12, 25], # Rotor VI (M, Z)
            [12, 25], # Rotor VII (M, Z)
            [12, 25], # Rotor VIII (M, Z)
            [],       # Rotor IX (Beta)
            []        # Rotor X (Gamma)
        ]

        reflectors = {
            'B': "ENKQAUYWJICOPBLMDXZVFTHRGS",  # Reflector B (B Thin)
            'C': "RDOBJNTKVEHMLFCWZAXGYIPSUQ"   # Reflector C (C Thin)
        }

        self.etw = list(range(26))

        chosen_rotors = [rotor_index_map[choice.upper()] for choice in rotor_choices]
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
        rotate_next = [False, False, False, False]

        # Check if the rightmost rotor hits its notch
        if self.positions[3] in self.turnovers[3]:
            rotate_next[2] = True

        # Check for double stepping mechanism
        if self.positions[2] in self.turnovers[2]:
            rotate_next[1] = True
            rotate_next[2] = True

        # Rotate the rightmost rotor
        self.positions[3] = (self.positions[3] + 1) % 26

        if rotate_next[2]:
            self.positions[2] = (self.positions[2] + 1) % 26

        if rotate_next[1]:
            self.positions[1] = (self.positions[1] + 1) % 26

        if rotate_next[0]:
            self.positions[0] = (self.positions[0] + 1) % 26

    def encode_char(self, char):
        char_index = self.plugboard[ord(char.upper()) - ord('A')]

        char_index = self.etw[char_index]

        self.rotate()

        for i in range(3, -1, -1):
            char_index = (self.rotors[i][(char_index + self.positions[i] - self.ring_settings[i]) % 26] -
                          self.positions[i] + self.ring_settings[i]) % 26

        char_index = self.reflector[char_index]

        for i in range(4):
            char_index = (self.rotors[i].index((char_index + self.positions[i] - self.ring_settings[i]) % 26) -
                          self.positions[i] + self.ring_settings[i]) % 26

        return chr(self.plugboard[char_index] + ord('A'))

    def encode(self, message):
        encoded = ''.join(self.encode_char(c) for c in message if c.isalpha())
        groups = [encoded[i:i + 4] for i in range(0, len(encoded), 4)]
        formatted = '\n'.join([' '.join(groups[i:i + 10]) for i in range(0, len(groups), 10)])
        return formatted

def setup_enigma():
    while True:
        reflector_choice = input("Choose reflector (B or C): ").strip()
        rotor_choices = input("Enter rotor choices (select 4 from I to X, e.g., IX VIII VI V): ").split()
        if len(rotor_choices) != 4:
            print("Please enter exactly 4 rotors.")
            continue
        if 'IX' in rotor_choices[1:] or 'X' in rotor_choices[1:]:
            print("Rotor IX (Beta) and Rotor X (Gamma) can only be used in the first position nearest to the reflector. Please reselect.")
            continue
        break

    ring_settings = input("Enter ring settings (4 letters, e.g., ABCD): ").strip()
    initial_positions = input("Enter initial positions (4 letters, e.g., ABCD): ").strip()
    plugboard_pairs = input("Enter plugboard pairs (up to 10 pairs separated by space, or 'none'): ").strip()
    plugboard_settings = [] if plugboard_pairs.lower() == 'none' else plugboard_pairs.split()

    enigma_machine = Enigma(rotor_choices, ring_settings, initial_positions, reflector_choice, plugboard_settings)
    plaintext = input("Enter the plaintext message to encode: ").strip()
    encoded_message = enigma_machine.encode(plaintext)
    print("Encoded message:\n", encoded_message)

setup_enigma()

import os

class MNT_Tuple:
    def __init__(self, name, index):
        self.Name = name
        self.Index = index

    def __str__(self):
        return f"[{self.Name}, {self.Index}]"


class MacroProcessor:
    MNT = []
    MDT = []
    MNT_Counter = 0
    MDT_Counter = 0
    MDT_P = 0
    Input = None
    ALA = []
    ALA_MacroBinding = {}

    @staticmethod
    def main(args):
        MacroProcessor.initialize_tables()
        print("===== PASS 1 =====\n")
        MacroProcessor.Pass1()
        print("\n===== PASS 2 =====\n")
        MacroProcessor.Pass2()

    @staticmethod
    def Pass1():
        with open("Input.txt", "r") as f:
            with open("OutputPass1.txt", "w") as output:
                for line in f:
                    if line.strip().upper() == "MACRO":
                        MacroProcessor.process_macro_definition(f)
                    else:
                        output.write(line)
                print("ALA:")
                MacroProcessor.show_ala(1)
                print("\nMNT:")
                MacroProcessor.show_mnt()
                print("\nMDT:")
                MacroProcessor.show_mdt()

    @staticmethod
    def process_macro_definition(f):
        line = f.readline().strip()
        macro_name = line.split()[0]
        MacroProcessor.MNT.append(MNT_Tuple(macro_name, MacroProcessor.MDT_Counter))
        MacroProcessor.MNT_Counter += 1
        MacroProcessor.Pass1ALA(line)

        # Add the macro header to MDT as it is (name and arguments unchanged)
        MacroProcessor.MDT.append(line)
        MacroProcessor.MDT_Counter += 1

        # Process the macro body and replace arguments with #1, #2, etc.
        MacroProcessor.add_into_mdt(len(MacroProcessor.ALA) - 1, f)

    @staticmethod
    def Pass1ALA(line):
        tokens = line.split()
        macro_name = tokens[0]
        param_list = [token.split('=')[0] for token in tokens[1:]]
        MacroProcessor.ALA.append(param_list)
        MacroProcessor.ALA_MacroBinding[macro_name] = len(MacroProcessor.ALA) - 1

    @staticmethod
    def add_into_mdt(ala_number, f):
        while True:
            line = f.readline().strip()
            if line.upper() == "MEND":
                MacroProcessor.MDT.append("MEND")  # Ensure MEND is added to MDT
                MacroProcessor.MDT_Counter += 1
                break
            temp_line = line.split()
            formatted_line = f"{temp_line[0]:<12}"

            # Process tokens in the macro body
            for token in temp_line[1:]:
                if token.startswith("&"):
                    # Find the parameter index in the ALA table
                    index = -1
                    for i, param in enumerate(MacroProcessor.ALA[ala_number]):
                        if token == param:
                            index = i
                            break
                    if index != -1:
                        formatted_line += f",#{index+1}"  # Corrected to #<index+1>
                    else:
                        formatted_line += f",?{token}"  # Use ?<token> as a placeholder
                else:
                    formatted_line += f",{token}"  # Keep non-argument tokens as they are

            MacroProcessor.MDT.append(formatted_line)
            MacroProcessor.MDT_Counter += 1

    @staticmethod
    def show_ala(pass_num):
        with open(f"OutputALA_Pass{pass_num}.txt", "w") as out:
            for lst in MacroProcessor.ALA:
                print(lst)
                out.write(f"{lst}\n")

    @staticmethod
    def show_mnt():
        with open("OutputMNT.txt", "w") as out:
            for mnt_tuple in MacroProcessor.MNT:
                print(mnt_tuple)
                out.write(f"{mnt_tuple}\n")

    @staticmethod
    def show_mdt():
        with open("OutputMDT.txt", "w") as out:
            for line in MacroProcessor.MDT:
                print(line)
                out.write(f"{line}\n")

    @staticmethod
    def Pass2():
        with open("OutputPass1.txt", "r") as f:
            with open("OutputPass2.txt", "w") as output:
                for line in f:
                    tokens = line.split()
                    if tokens:
                        token = tokens[0]
                        mnt_tuple = next((m for m in MacroProcessor.MNT if m.Name == token), None)
                        if mnt_tuple:
                            MacroProcessor.MDT_P = mnt_tuple.Index
                            ala_list = MacroProcessor.Pass2ALA(line)
                            MacroProcessor.MDT_P += 1
                            while True:
                                if MacroProcessor.MDT_P >= len(MacroProcessor.MDT):
                                    print("Warning: MDT pointer exceeded the list length.")
                                    break
                                mdt_line = MacroProcessor.MDT[MacroProcessor.MDT_P].strip()
                                if mdt_line.upper() == "MEND":
                                    break
                                formatted_line = f"{mdt_line:<12}"
                                mdt_tokens = mdt_line.split()
                                for mdt_token in mdt_tokens[1:]:
                                    if mdt_token.startswith("#"):
                                        index = int(mdt_token[1:])
                                        formatted_line += f",{ala_list[index-1]}"
                                output.write(f"{formatted_line}\n")
                                print(formatted_line)
                                MacroProcessor.MDT_P += 1
                        else:
                            output.write(line)
                            print(line)
                print("\nALA:")
                MacroProcessor.show_ala(2)

    @staticmethod
    def Pass2ALA(line):
        tokens = line.split()
        macro_name = tokens[0]
        ala_no = MacroProcessor.ALA_MacroBinding[macro_name]
        ala_list = MacroProcessor.ALA[ala_no]

        # Initialize counter for matching parameters in the ALA
        counter = 0
        try:
            # Process the parameters from the line
            params = tokens[1].split(',')
            for param in params:
                # Ensure the list is large enough
                if counter >= len(ala_list):
                    ala_list.append("")  # Extend the list if necessary
                ala_list[counter] = param
                counter += 1
        except Exception as e:
            pass

        # Handle remaining tokens, including those with '='
        if counter < len(tokens):
            mdt_line = MacroProcessor.MDT[MacroProcessor.MDT_P]
            mdt_tokens = mdt_line.split()
            for mdt_token in mdt_tokens:
                if '=' in mdt_token:
                    # Ensure the list is large enough before assigning
                    if counter >= len(ala_list):
                        ala_list.append("")  # Extend the list if necessary
                    ala_list[counter] = mdt_token.split('=')[1]
                    counter += 1

        # Update ALA with the modified list
        MacroProcessor.ALA[ala_no] = ala_list
        return ala_list

    @staticmethod
    def initialize_tables():
        MacroProcessor.MNT = []
        MacroProcessor.MDT = []
        MacroProcessor.ALA = []
        MacroProcessor.ALA_MacroBinding = {}
        MacroProcessor.MNT_Counter = 0
        MacroProcessor.MDT_Counter = 0


# To run the program
if __name__ == "__main__":
    MacroProcessor.main([])

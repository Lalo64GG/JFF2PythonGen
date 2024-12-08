import xml.etree.ElementTree as ET

def parse_jff(file_path):
    tree = ET.parse(file_path, parser=ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()
    
    # Extraer estados
    states = {}
    for state in root.find("automaton").findall("state"):
        state_id = state.get("id")
        state_name = state.get("name")
        is_initial = state.find("initial") is not None
        is_final = state.find("final") is not None
        states[state_id] = {
            "name": state_name,
            "is_initial": is_initial,
            "is_final": is_final,
        }
    
    # Extraer transiciones
    transitions = []
    for transition in root.find("automaton").findall("transition"):
        from_state = transition.find("from").text
        to_state = transition.find("to").text
        read_symbol = transition.find("read").text or ''  # Manejar transiciones con épsilon
        transitions.append({
            "from": states[from_state]["name"],
            "to": states[to_state]["name"],
            "symbol": read_symbol
        })
    
    return states, transitions

def generate_python_code(states, transitions):
    # Buscar el estado inicial
    initial_state = next(state["name"] for state in states.values() if state["is_initial"])
    final_states = [state["name"] for state in states.values() if state["is_final"]]
    
    # Generar el código como un string
    code = "# -*- coding: utf-8 -*-\n\n"
    code += "class Automata:\n"
    code += "    def __init__(self):\n"
    code += f"        self.state = '{initial_state}'\n"
    code += f"        self.final_states = {final_states}\n"
    code += "        self.transitions = {\n"
    
    # Construir el diccionario de transiciones
    transition_dict = {}
    for t in transitions:
        key = (t["from"], t["symbol"])
        transition_dict[key] = t["to"]
    for key, value in transition_dict.items():
        code += f"            ('{key[0]}', '{key[1]}'): '{value}',\n"
    code += "        }\n\n"
    
    code += "    def transition(self, symbol):\n"
    code += "        key = (self.state, symbol)\n"
    code += "        if key in self.transitions:\n"
    code += "            self.state = self.transitions[key]\n"
    code += "        else:\n"
    code += "            self.state = ''  # Estado de rechazo\n\n"
    
    code += "    def is_accepting(self):\n"
    code += "        return self.state in self.final_states\n\n"
    
    code += "def test_automata(input_string):\n"
    code += "    automata = Automata()\n"
    code += "    for symbol in input_string:\n"
    code += "        automata.transition(symbol)\n"
    code += "    return automata.is_accepting()\n"
    return code

# Leer y parsear el archivo JFF
file_path = "Automata_Lalo-2.jff"  # Cambiar por la ruta del archivo JFF
states, transitions = parse_jff(file_path)

# Generar el código Python
python_code = generate_python_code(states, transitions)

# Guardar el código en un archivo
with open("automata.py", "w", encoding="utf-8") as f:
    f.write(python_code)

print("¡Código generado exitosamente!")

import io
def write_well_info(result, out="output.txt"):
    with open(out, "a") as f:
        f.write('Well Information\n')
        f.write('NAME | UNIT | VALUE | DESCRIPTION\n')
        for param in result:
            line = f"{param['name']},{param['unit']},{param['value']},{param['description']}\n"
            f.write(line)

def write_curve_info(result, out="output.txt"):
    with open(out, "a") as f:
        f.write('Curve Information\n')
        f.write('NAME | UNIT | DESCRIPTION\n')
        for param in result:
            line = f"{param['name']},{param['unit']},{param['description']}\n"
            f.write(line)

def write_curve_data(result, out="output.txt"):
    with open(out, "a") as f:
        f.write('ASCII\n')
        for mnemonic, values in result:
            line = f"{mnemonic}: {', '.join(values)}\n"
            f.write(line)
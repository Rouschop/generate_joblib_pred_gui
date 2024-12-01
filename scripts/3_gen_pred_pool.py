import sys
import joblib
import numpy as np
import itertools
from multiprocessing import Pool

MAX_ARGS = 100
MAX_COMBOS = 100000
BUFFER_SIZE = 256

class Feature:
    def __init__(self, name, min_val, max_val, step):
        self.name = name
        self.min = min_val
        self.max = max_val
        self.step = step

class Constant:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def parse_feature(arg):
    try:
        name, range_str = arg.split('=')
        min_val, max_val, step = map(float, range_str.split(','))
        return Feature(name, min_val, max_val, step)
    except ValueError:
        return None

def parse_constant(arg):
    try:
        name, value_str = arg.split('=')
        value = float(value_str)
        return Constant(name, value)
    except ValueError:
        return None

def print_help():
    print("""
Usage: python generate_combinations.py [OPTIONS]

Options:
  --feature <name>=<min>,<max>,<step>   Specify feature ranges (e.g., --feature feature1=0,10,2)
  --constant <name>=<value>             Specify constant values (e.g., --constant constant1=3.14)
  --model <model_path>                  Load a trained model (in joblib format) for predictions
  --o <output_file>                     Output CSV file to store the combinations and predictions
  --help                               Show this help message
  """)

def generate_combinations(features, constants, arg_order, output_file, model=None):
    total_combinations = 1

    feature_ranges = []
    for feature in features:
        steps = int((feature.max - feature.min) / feature.step) + 1
        feature_ranges.append(np.arange(feature.min, feature.max + feature.step, feature.step))
        total_combinations *= steps

    if total_combinations > MAX_COMBOS:
        print("Too many combinations. Reduce the range or step size.")
        sys.exit(1)

    all_combinations = list(itertools.product(*feature_ranges))

    rows = []
    for combo in all_combinations:
        row = []
        for arg in arg_order:
            if any(arg == feature.name for feature in features):
                feature = next(f for f in features if f.name == arg)
                value = combo[features.index(feature)]
                try:
                    value = float(value)
                    row.append(f"{value:.6f}")
                except ValueError:
                    row.append(str(value))
            elif any(arg == constant.name for constant in constants):
                constant = next(c for c in constants if c.name == arg)
                row.append(f"{constant.value:.6f}")

        rows.append(row)

    if model:
        chunk_size = max(1, len(rows) // (Pool()._processes or 4))
        chunks = [rows[i:i + chunk_size] for i in range(0, len(rows), chunk_size)]

        with Pool() as pool:
            predictions = pool.map(process_chunk, [(chunk, features, constants, model) for chunk in chunks])

        predictions = [item for sublist in predictions for item in sublist]

        for i, row in enumerate(rows):
            rows[i] = row + [predictions[i]]

    try:
        with open(output_file, "w") as fp:
            fp.write(",".join(arg_order) + ",prediction\n")
            for row in rows:
                fp.write(",".join(f"{x:.6f}" if isinstance(x, (int, float)) else str(x) for x in row) + "\n")

        print(f"Combinations saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def process_chunk(args):
    chunk, features, constants, model = args
    results = []
    for row in chunk:
        feature_values = [float(row[features.index(f)]) for f in features]
        constant_values = [constant.value for constant in constants]

        input_features = np.array(feature_values + constant_values).reshape(1, -1)
        
        try:
            prediction = model.predict(input_features)[0]
            results.append(prediction)
        except Exception as e:
            print(f"Error during prediction: {e}")
            results.append(None)

    return results

def main():
    features = []
    constants = []
    arg_order = []
    f_count = 0
    c_count = 0

    output_file = None
    model = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith("--feature"):
            if f_count >= MAX_ARGS:
                print("Too many features specified.")
                sys.exit(1)

            feature = parse_feature(sys.argv[i + 1])
            if not feature:
                print(f"Invalid feature format: {sys.argv[i + 1]}")
                sys.exit(1)
            features.append(feature)
            arg_order.append(feature.name)
            f_count += 1
            i += 2
        elif sys.argv[i].startswith("--constant"):
            if c_count >= MAX_ARGS:
                print("Too many constants specified.")
                sys.exit(1)

            constant = parse_constant(sys.argv[i + 1])
            if not constant:
                print(f"Invalid constant format: {sys.argv[i + 1]}")
                sys.exit(1)
            constants.append(constant)
            arg_order.append(constant.name)
            c_count += 1
            i += 2
        elif sys.argv[i].startswith("--model"):
            model_path = sys.argv[i + 1]
            try:
                model = joblib.load(model_path)
                print(f"Model loaded from {model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
                sys.exit(1)
            i += 2
        elif sys.argv[i].startswith("--o"):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--help":
            print_help()
            sys.exit(0)
        else:
            print(f"Unknown argument: {sys.argv[i]}")
            sys.exit(1)

    if not output_file:
        print("Output file must be specified with --o")
        sys.exit(1)

    generate_combinations(features, constants, arg_order, output_file, model)

if __name__ == "__main__":
    main()

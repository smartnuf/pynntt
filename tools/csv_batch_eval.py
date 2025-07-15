import csv
import sympy as sp
from pathlib import Path
import argparse
from pynntt.networks import parse_descriptor, eval_impedance, canonical_form


def load_catalogue(path):
    """Read a CSV catalogue of networks. Assumes 'ID' and 'Desc' columns."""
    rows = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'ID' not in row or 'Desc' not in row:
                raise ValueError("CSV must contain 'ID' and 'Desc' headers")
            rows.append({'id': row['ID'].strip(), 'desc': row['Desc'].strip()})
    return rows


def evaluate_catalogue(rows):
    """Evaluate each network's impedance and return enriched rows."""
    enriched = []
    for row in rows:
        try:
            ast = parse_descriptor(row['desc'])
            Z = eval_impedance(ast)
            Zcanon = canonical_form(Z)
            enriched.append({**row, 'ast': ast, 'Z': Z, 'Zcanon': Zcanon})
        except Exception as e:
            enriched.append({**row, 'error': str(e)})
    return enriched


def save_results_csv(rows, path):
    """Save canonical Z(s) results to a CSV."""
    keys = ['id', 'desc', 'Zcanon', 'error']
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            out = {k: row.get(k, '') for k in keys}
            writer.writerow(out)


def main():
    parser = argparse.ArgumentParser(description="Evaluate network impedances from a descriptor CSV.")
    parser.add_argument("input_csv", type=str, help="Path to input CSV with 'ID' and 'Desc' columns")
    parser.add_argument("output_csv", type=str, help="Path to write output CSV with results")
    args = parser.parse_args()

    input_file = Path(args.input_csv)
    output_file = Path(args.output_csv)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    catalogue = load_catalogue(input_file)
    results = evaluate_catalogue(catalogue)
    save_results_csv(results, output_file)
    print(f"Processed {len(results)} entries to {output_file}")


if __name__ == '__main__':
    main()

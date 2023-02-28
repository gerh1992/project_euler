import argparse
from utils.problemas import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--problema",
        help="Solucion a problema numero ? en projecteuler.net",
        type=int,
        required=True
    )
    args = parser.parse_args()
    try:
        print(globals()[f"problema_{args.problema}"]())
    except Exception as e:
        print(str(e))
        print(f"Problema {args.problema} no existe")
        raise e


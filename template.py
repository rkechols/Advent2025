from utils import get_input_file_path


def main():
    with open(get_input_file_path(), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                pass
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise


if __name__ == "__main__":
    main()

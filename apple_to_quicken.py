import csv
import sys


def munge_apple_card_csv(input_file, output_file):
    quicken_headers = [
        "date",
        "payee",
        "fipayee",
        "amount",
        "debit/credit",
        "category",
        "account",
        "tag",
        "memo",
        "chknum",
    ]

    try:
        with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)

            with open(
                output_file, mode="w", newline="", encoding="utf-8"
            ) as outfile:
                writer = csv.DictWriter(outfile, fieldnames=quicken_headers)
                writer.writeheader()

                for row in reader:
                    # 1. Concatenate Type, Category, and Description for the memo
                    # (Keeping Apple's category here so you can still see it for reference!)
                    trans_type = row.get("Type", "").strip()
                    category = row.get("Category", "").strip()
                    description = row.get("Description", "").strip()

                    memo_parts = [trans_type, category, description]
                    memo_value = " - ".join([p for p in memo_parts if p])

                    # 2. Adjust the amount sign (Apple positive -> Quicken negative)
                    raw_amount = row.get("Amount (USD)", "").strip()
                    quicken_amount = ""

                    if raw_amount:
                        try:
                            flipped_amount = float(raw_amount) * -1
                            quicken_amount = f"{flipped_amount:.2f}"
                        except ValueError:
                            quicken_amount = raw_amount

                    # 3. Build the new row matching Quicken's schema
                    quicken_row = {
                        "date": row.get("Transaction Date"),
                        "payee": row.get("Merchant"),
                        "fipayee": "",
                        "amount": quicken_amount,
                        "debit/credit": "",
                        "category": "",  # FORCED BLANK: Prevents Quicken from creating duplicate categories
                        "account": "Apple Card",
                        "tag": "",
                        "memo": memo_value,  # You can still see Apple's original category here
                        "chknum": "",
                    }

                    writer.writerow(quicken_row)

        print(f"Success! File converted and saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' could not be found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python apple_to_quicken.py <input_file.csv> <output_file.csv>")
    else:
        munge_apple_card_csv(sys.argv[1], sys.argv[2])

# pylint: disable=invalid-name

"""
computeSales.py

This script computes the total cost of sales based on a price catalogue
and sales records. It is designed to be invoked from the command line,
taking two JSON files as input parameters: a price catalogue file and
a sales record file.

Usage:
    python computeSales.py priceCatalogue.json salesRecord.json

Functions:
    - load_json_file(filename): Load JSON data from a file.
    - compute_total_cost(price_catalogue, sales_record): Compute total
        sales cost based on price catalogue.
    - main(): Main function to handle command line arguments, compute sales
        cost, and print results.

Requirements:
    1. The program must be invoked from the command line.
    2. Results shall be printed on the screen and saved to
        a file named SalesResults.txt.
    3. The script shall receive two files as parameters:
        a price catalogue and a sales record.
    4. If a product in the sales record is not found
        in the price catalogue, a warning is issued.
    5. Results include a tabular format with product,
        quantity, and total unit cost.
    6. Include time elapsed for execution and calculation
        of data in results.

"""

import json
import sys
import time


def load_json_file(filename):
    """Load JSON data from a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")
        return None


def compute_total_cost(price_catalogue, sales_record):
    """Compute the total cost for all sales based
        on price catalogue."""
    total_cost = 0
    total_quantity = 0
    unitary_cost = {}

    price_catalogue_dict = {item['title']: item['price']
                            for item in price_catalogue}

    for sale in sales_record:
        product_sold = sale['Product']
        quantity = sale['Quantity']

        if product_sold in price_catalogue_dict:
            item_price = price_catalogue_dict[product_sold]
            total_cost += item_price * quantity
            total_quantity += quantity
            if product_sold not in unitary_cost:
                unitary_cost[product_sold] = [quantity, item_price * quantity]
            else:
                # Increase quantity
                unitary_cost[product_sold][0] += quantity
                # Increase total cost per product
                unitary_cost[product_sold][1] += item_price * quantity
        else:
            print(f"Warning: Product ID '{product_sold}' not found "
                  f"in the price catalogue.")
    return total_cost, total_quantity, unitary_cost


def main():
    """Main function to compute total sales cost and write results."""
    # Requirement 5: The program shall be invoked from a command line.
    # Requirement 6: The program shall receive two files as parameters.
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py "
              "priceCatalogue.json salesRecord.json")
        return

    start_time = time.time()

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    price_catalogue = load_json_file(price_catalogue_file)
    if price_catalogue is None:
        return

    sales_record = load_json_file(sales_record_file)
    if sales_record is None:
        return

    (total_cost,
     total_amount,
     unitary_cost) = compute_total_cost(price_catalogue,
                                        sales_record)

    end_time = time.time()
    elapsed_time = end_time - start_time

    line_sep_str = "+" + "-" * 32 + "+" + "-" * 32 + "+" + "-" * 32 + "+\n"

    # Build printing results in tabular format
    report_str = ''
    report_str += line_sep_str
    report_str += (f"| {'Product':^30} | {'Quantity':^30} | "
                   f"{'Total Unit Cost':^30} |\n")
    report_str += line_sep_str
    for product_sold, total_unit_cost in unitary_cost.items():
        report_str += (f"| {f'{product_sold}':>30} | "
                       f"{f'{total_unit_cost[0]}':>30} | "
                       f"{'$' + f'{total_unit_cost[1]:.2f}':>30} |\n")
    report_str += line_sep_str
    report_str += (f"| {'Total Cost of Sales':<30} | "
                   f"{f'{total_amount}':>30} | "
                   f"{'$' + f'{total_cost:.2f}':>30} |\n")
    report_str += line_sep_str
    report_str += ((f"| {'Time Elapsed':<30} | "
                    f"{f'{elapsed_time:.6f} seconds':>30} |") +
                   'x' * 32 + "|\n")
    report_str += line_sep_str
    print(report_str)

    # Requirement 2: The results shall be printed on the screen and on
    # a file named SalesResults.txt.
    # Requirement 7: Include time elapsed for execution and calculation
    # of data in results.
    # Writing results to file

    with open("SalesResults.txt", 'w', encoding='utf-8') as results_file:
        results_file.write(report_str)


if __name__ == "__main__":
    main()

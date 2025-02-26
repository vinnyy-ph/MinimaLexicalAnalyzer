# python
import openpyxl
from lark import Lark

def main():
    # Load the Lark grammar from the file "grammar.lark"
    parser = Lark.open("grammar.lark", start="start", parser="lalr")
    
    # Get the list of all terminal symbols (expected tokens)
    terminals = parser.terminals

    # Create a new Excel workbook and set active worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Expected Tokens"

    # Write header row
    sheet.append(["Token Name", "Regex/Pattern"])

    # Write each terminal's information into rows
    for term in terminals:
        # term.pattern is a Pattern object, so we convert it to string.
        pattern_str = str(term.pattern)
        sheet.append([term.name, pattern_str])

    # Save the workbook to an Excel file
    workbook.save("expected_tokens.xlsx")
    print("Excel file 'expected_tokens.xlsx' was created successfully.")

if __name__ == "__main__":
    main()
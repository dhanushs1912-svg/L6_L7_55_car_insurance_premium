"""Car insurance premium input parser - hardened against invalid input.

Name: Dhanush S   SRN: PES1UG24AM360   Section: F

Every function below originally assumed its input was a well formed string.
Hypothesis fuzzing showed that each one crashed on None, on an empty string
and on malformed text. They now validate their input first and return a safe
value instead of raising, while behaving exactly as before on valid input.
"""


def normalize_registration(plate):
    """Remove spaces, dashes and dots from a registration and upper-case it.

    Bug found by fuzzing: `None` (or any non-string) raised AttributeError on
    `.strip()`. Anything that is not a string now returns an empty string.
    """
    if not isinstance(plate, str):
        return ""
    plate = plate.strip().upper()
    for ch in [' ', '-', '.']:
        plate = plate.replace(ch, '')
    return plate


def total_claim_amount(text):
    """Add up claim amounts separated by semicolons.

    Bugs found by fuzzing: `None` raised AttributeError on `.split()`, and an
    empty string or a non-numeric part such as "12000;;800" or "abc" raised
    ValueError inside `int()`. Parts that are not a valid non-negative whole
    number are now skipped, so the total is always a number.
    """
    if not isinstance(text, str):
        return 0
    total = 0
    for part in text.split(';'):
        part = part.strip()
        if not part:
            continue
        try:
            amount = int(part)
        except ValueError:
            continue
        if amount >= 0:
            total += amount
    return total


def driver_age(dob, current_year=2026):
    """Work out a driver's age from a DD/MM/YYYY date of birth.

    Bugs found by fuzzing: `None` raised AttributeError on `.split()`, a string
    without two slashes such as "" or "14/08" raised IndexError on `[2]`, and a
    non-numeric year such as "14/08/abcd" raised ValueError. The date is now
    validated and `None` is returned when the age cannot be worked out.
    """
    if not isinstance(dob, str):
        return None
    parts = dob.split('/')
    if len(parts) != 3:
        return None
    year_text = parts[2].strip()
    if not year_text.isdigit():
        return None
    age = current_year - int(year_text)
    if age < 0 or age > 120:
        return None
    return age


def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    print("Normalized registration:", normalize_registration(value))

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    print("Total claimed:", total_claim_amount(value))

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    print("Driver age in 2026:", driver_age(value))


if __name__ == "__main__":
    main()

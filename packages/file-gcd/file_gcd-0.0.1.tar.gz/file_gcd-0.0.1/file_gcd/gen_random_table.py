import pandas as pd
import random
import string


def generate_random_property(length=8):
    """Generates a random numeric string of a given length."""
    return ''.join(random.choices(string.digits, k=length))


def generate_random_data(num_rows=100, num_numeric_cols=3):
    """Generates a DataFrame with random data.

    PROPERTY: Random 8-character strings
    NUM1, NUM2, ..., NUMn: Random integers between 1 and 100
    """
    # Generate 100 rows of random 8-character strings for PROPERTY
    data = {
        'ID': [i for i in range(num_rows)],
        'PROPERTY': [generate_random_property() for _ in range(num_rows)]
    }

    # Add random numeric columns (NUM1, NUM2, ...)
    for i in range(1, num_numeric_cols + 1):
        data[f'NUM{i}'] = [random.randint(1, 100) for _ in range(num_rows)]

    return pd.DataFrame(data)


def main():
    # Generate the random data
    df = generate_random_data(num_rows=100, num_numeric_cols=3)

    # Output the first few rows to verify the result
    print(df.head())

    # Optionally, save to a CSV file
    df.to_csv('generated_data.csv', index=False)


if __name__ == "__main__":
    main()

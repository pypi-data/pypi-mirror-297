import pandas as pd
import click


@click.command()
@click.argument('filename', type = click.Path(exists=True))
@click.option('--verbose', '-v', is_flag = True)
def main(filename, verbose):
    if verbose:
        print("In verbose mode")
    """
    this function is used to lint a csv file
    """
    df = pd.read_csv(filename)
    for column in zero_count_columns(df):
        click.echo(f"Warning: Column '{column}' has no item in it")
    unnamed = unnamed_columns(df)
    if unnamed:
        click.echo(f"Warning: found '{unnamed}' columns that are unnamed")
    carriage_field = carriage_returns(df)
    if carriage_field:
        index, column, field = carriage_field
        click.echo((
            f"Warning: found carriage returns at index {index}"
            f" of column '{column}': "
        ))
        print((f"                   '{field[:50]}'"))
def unnamed_columns(df):
    bad_columns = []
    for key in df.keys():
        if "Unnamed" in key:
            bad_columns.append(key)
    return len(bad_columns)

def zero_count_columns(df):
    bad_columns = []
    for key in df.keys():
        if df[key].count() == 0:
            bad_columns.append(key)
    return bad_columns

def carriage_returns(df: pd.DataFrame):
    for index, row in df.iterrows():
        for column, field in row.items():
            try:
                if "\r\n" in field:
                    return index, column, field
            except:
                continue

    pass 


if __name__ == '__main__':
    main()
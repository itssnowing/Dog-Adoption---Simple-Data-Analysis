import pandas as pd


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):

    # keep only these columns
    cols_to_keep = [
        'id',
        'species',
        'breed_primary',
        'breed_secondary',
        'breed_mixed',
        'breed_unknown',
        'age',
        'name',
        'posted',
        'contact_city',
        'contact_state',
        'contact_zip',
    ]

    # grab the historical Petfinder csv
    df = pd.read_csv('https://query.data.world/s/ya55hgvcoyseazrafkmear736cbxi6?dws=00000',
                     usecols=cols_to_keep)


    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

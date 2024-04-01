import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # parse_dates struggles with the format of the posted column
    # remove the timezone information because I only care about the date
    data['posted'] = pd.to_datetime(data['posted'], errors='coerce').dt.tz_localize(None).dt.strftime('%Y-%m-%d')

    # I want to partitiion my data by year & month, prepping it here for ease
    data['CALC_Year'] = data['posted'].str[:4]
    data['CALC_Month'] = data['posted'].str[5:7]
    
    # the data is skewed
    # drop rows where the values are not 2 letters
    data = data[(data['contact_state'].str.isalpha()) & (data['contact_state'].str.len() == 2)]

    # drop rows from before 2017 as they are assumed outdated or wrong
    data = data[pd.to_datetime(data['posted']).dt.year > 2017]

    # clean up and normalize pet names, names with spaces are assumed to use the first as the primary
    data = data[data['name'].notnull()]
    data['name'] = data['name'].str.replace('[^\w\s]', '').str.upper()
    data['name'] = data['name'].str.partition(' ')[0]

    # breed normalizers
    # these are based generally on how shelters classify dogs, they aren't necessarily accurate to real breeds
    pitbulls = ['Pit Bull Terrier', 'Staffordshire Bull Terrier', 'American Staffordshire Terrier',
                'Bull Terrier', 'American Bully', 'American Bulldog', 'Boxer']

    hounds = ['Black Mouthed Cur', 'Mountain Cur']

    mixed_breed = ['Collie', 'Terrier', 'Spaniel', 'Shepherd']

    # overwrite breed info
    data[['breed_primary', 'breed_secondary']].fillna('NA', inplace=True)

    data.loc[data['breed_primary'].isin(pitbulls), 'breed_primary'] = 'Pitbull'
    data.loc[data['breed_secondary'].isin(pitbulls), 'breed_secondary'] = 'Pitbull'

    data.loc[data['breed_primary'] == 'Smooth Collie', 'breed_primary'] = 'Rough Collie'
    data.loc[data['breed_secondary'] == 'Smooth Collie', 'breed_secondary'] = 'Rough Collie'

    data.loc[data['breed_primary'].str.contains('Labrador Retriever', na=False), 'breed_primary'] = 'Labrador'
    data.loc[data['breed_secondary'].str.contains('Labrador Retriever', na=False), 'breed_secondary'] = 'Labrador'

    data.loc[data['breed_primary'].isin(hounds), 'breed_primary'] = 'Hound'
    data.loc[data['breed_secondary'].isin(hounds), 'breed_secondary'] = 'Hound'
    data.loc[data['breed_primary'].str.contains('Coonhound', na=False), 'breed_primary'] = 'Hound'
    data.loc[data['breed_secondary'].str.contains('Coonhound', na=False), 'breed_secondary'] = 'Hound'

    data.loc[data['breed_primary'].isin(mixed_breed), 'breed_primary'] = 'Mixed Breed'
    data.loc[data['breed_secondary'].isin(mixed_breed), 'breed_secondary'] = 'Mixed Breed'

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def test_blank_state(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['contact_state'].isin(['', pd.NA]).sum() == 0, 'There are blank states'

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['contact_state'].str.isnumeric().sum() == 0, 'There are invalid states'

@test
def test_name(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['name'].isnull().sum() == 0, 'There are pets with no name'

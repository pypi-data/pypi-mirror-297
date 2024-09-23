import pandas as pd
import pytest

from rgc.utils.data import catalog_quest


def test_catalog_quest(mocker):
    # Mock the Vizier object and its methods
    mock_vizier = mocker.patch("rgc.utils.data.Vizier")
    mock_catalog = mocker.MagicMock()
    mock_catalog.to_pandas.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    mock_vizier.get_catalogs.return_value = [mock_catalog]

    # Call the function
    result = catalog_quest("some_catalog", service="Vizier")

    # Verify the result
    expected_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    pd.testing.assert_frame_equal(result, expected_df)
    mock_vizier.get_catalogs.assert_called_once_with("some_catalog")


def test_catalog_quest_unsupported_service():
    with pytest.raises(Exception, match="Unsupported service provided. Only 'Vizier' is supported."):
        catalog_quest("some_catalog", service="UnsupportedService")

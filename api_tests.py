import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from spoonacular import recipe_search


class RecipeSearchTests(unittest.TestCase):
    # This test makes sure that the api call is functioning
    def test_only_ingredients(self):
        expected_ingredients = ["apple"]
        expected_cuisine = []
        expected_diet = []
        expected_intolerances = []
        not_expected_output = ([], [], [])

        mock_response = [MagicMock(), MagicMock()]
        mock_response[0].json.return_value = {
            "results": [
                {
                    "id": 78673,
                }
            ]
        }
        mock_response[1].json.return_value = [
            {
                "id": 78673,
                "title": "title_exists",
                "image": "image_exists",
                "sourceUrl": "source_exists",
            }
        ]

        with patch(
            "spoonacular.requests.get", side_effect=[mock_response[0], mock_response[1]]
        ) as mock_requests_get:
            mock_requests_get.return_value = mock_response

            actual_output = recipe_search(
                expected_ingredients,
                expected_cuisine,
                expected_diet,
                expected_intolerances,
            )

            self.assertNotEqual(not_expected_output, actual_output)

    # This test makes sure that the api call doesn't function if given wrong paramaters
    def test_fotgotten_input(self):
        expected_ingredients = None
        expected_cuisine = []
        expected_diet = []
        expected_intolerances = []

        mock_response = [MagicMock(), MagicMock()]
        mock_response[0].json.return_value = {
            "results": [
                {
                    "id": 78673,
                }
            ]
        }
        mock_response[1].json.return_value = [
            {
                "id": 78673,
                "title": "title_exists",
                "image": "image_exists",
                "sourceUrl": "source_exists",
            }
        ]

        with patch(
            "spoonacular.requests.get", side_effect=[mock_response[0], mock_response[1]]
        ) as mock_requests_get:
            mock_requests_get.return_value = mock_response
            with self.assertRaises(TypeError):
                recipe_search(
                    expected_ingredients,
                    expected_cuisine,
                    expected_diet,
                    expected_intolerances,
                )


if __name__ == "__main__":
    unittest.main()

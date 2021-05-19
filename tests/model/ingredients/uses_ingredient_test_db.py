# from unittest import TestCase
#
# import persistence
# import tests
#
#
# class UsesIngredientTestDB(TestCase):
#     original_db_path: str = persistence.configs.path_into_db
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         # Patch the configs to point at the ingredient database;
#         persistence.configs.path_into_db = tests.configs.path_into_db
#
#     @classmethod
#     def tearDownClass(cls) -> None:
#         # Undo the patch;
#         persistence.configs.path_into_db = cls.original_db_path

from ._preprocessing import Preprocessor
from ..sql.generator import  multicol


class TargetEncoder(Preprocessor):
    """
    Replacing categorical variables with the average target variable values.

    Encoders are fitted in sklearn.

    Parameters:
    -----------
    target_var : str, default None
        The target variable name used for encoding. Must be set.
    categories : "auto" or list, default="auto"
        Categories per feature. If "auto", categories are determined from the data. (from sklearn)
    target_type : {"auto","continuous", "binary", "multiclass"}, default="binary"
        Type of the target variable. (from sklearn)
    smooth : "auto" or float, default="auto"
        Amount of smoothing between category means and the global mean. (from sklearn)
    cv : int, default=5
        Number of folds for cross-validation during fit. (from sklearn)
    shuffle : bool, default=True
        Whether to shuffle data before splitting into folds. (from sklearn)
    random_state : int or None, default=None
        Controls the randomness of shuffling when `shuffle=True`. (from sklearn)

    Raises:
    -------
    AssertionError:
        If `target_var` is None, or if `categories` or `target_type` are invalid.


    """
    def __init__(self, target_var=None, categories = 'auto', target_type = 'auto', smooth = 'auto', cv = 5,
                 shuffle = True, random_state = None):

        assert target_var is not None, "target_var must be specified"
        assert (isinstance(categories, list) and len(categories)>1) or (categories=="auto"), \
            "categories must be a list with more than one element or 'auto'"
        assert target_type in  ["auto","continuous","binary","multiclass"], \
            "target_type must be one of ['auto', 'continuous', 'binary', 'multiclass']"

        self.target_var = target_var
        self.categories = categories
        self.target_type = target_type
        self.smooth = smooth
        self.cv = cv
        self.shuffle = shuffle
        self.random_state = random_state

        self._output_col_formula = None
        self._output_col_name = None

        self.necessary_statistics = self.define_necessary_statistics()

    def __str__(self):
        return "TargetEncoder"

    def define_necessary_statistics(self):
        return [("TARGET", self.target_var, self.categories, self.target_type, self.smooth, self.cv, self.shuffle,
                    self.random_state)]

    def generate_sql_columns(self, prev_col_names_internal: list[str], prev_col_names: list[str],
                             fitted_statistics: dict) -> list[str]:

        output_col_formula = []
        output_col_name = []

        for (prev_col_name_internal, prev_col_name) in zip(prev_col_names_internal, prev_col_names):
            encoder_dict = fitted_statistics[prev_col_name]['encoder_dict']

            sql_list_tuples = multicol.target_encoder(prev_col_name_internal, prev_col_name, encoder_dict)

            [col_formula, col_name] = [list(t) for t in zip(*sql_list_tuples)]

            output_col_formula += col_formula
            output_col_name += col_name


        self._output_col_formula = output_col_formula
        self._output_col_name = output_col_name

        return self._output_col_formula


    def needs_subquery(self):
        return True

    def are_output_columns_different(self):
        return True

    def get_output_tdtype(self, input_tdtype=None) -> str:
        return "FLOAT()"

    def generate_column_output_names(self, fitted_statistics: dict) -> list[str]:
        #generate_sql_columns must be called first
        assert self._output_col_name is not None
        return self._output_col_name

    def generate_column_output_tdtypes(self, input_tdtypes, fitted_statistics: dict) -> list[str]:

        # important only for those functions where are_output_columns_different == True
        return ["FLOAT()" for i in range(len(self._output_col_name))]

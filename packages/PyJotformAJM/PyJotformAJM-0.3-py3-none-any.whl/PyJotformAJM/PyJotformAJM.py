"""
PyJotformAJM.py

"""
from jotform import JotformAPIClient
from ApiKeyAJM import APIKey

from datetime import datetime
from logging import getLogger
from typing import Union, Optional
from urllib.error import HTTPError


class JotFormAuthenticationError(HTTPError):
    ...


class NoJotformClientError(Exception):
    ...


class JotForm(APIKey):
    """
    This module defines a class `JotForm` that inherits from `APIKey`.

    The `JotForm` class represents an object that interacts with the JotForm API to retrieve and manipulate form data.

    Attributes:
    - `DEFAULT_FORM_ID`: A class attribute that represents the default form ID. It is set to `None` by default.
    - `ILLEGAL_STARTING_CHARACTERS`: A class attribute that represents the list of illegal starting characters for field
        names. It is set to `['<']` by default.
    - `IGNORED_FIELD_MESSAGE`: A class attribute that represents the error message displayed when a field is ignored
        due to an illegal starting character. It is set to `"ignored due to illegal starting character"` by default.

    Methods:
    - `__init__(self, **kwargs)`: Initializes an instance of `JotForm` with the given keyword arguments.
    - `_initialize_client(self)`: Initializes the JotForm client object.
    - `_validate_client(self)`: Validates the JotForm client object.
    - `_get_last_submission_id(self, last_sub_datetime: Union[datetime, str])`: Retrieves the last submission ID based
                                                                            on the provided last submission datetime.
    - `get_new_submissions(self)`: Returns the new submissions for a given form.
    - `_strip_answer(answer: Optional[Union[str, dict]])`: Strips leading and trailing whitespace from an answer.

    Properties:
    - `real_jf_field_names(self)`: Gets a list of field names extracted from the answers of a JotForm submission.
    - `form_section_headers(self)`: Gets a list of field names from a submission's answers where the field type is 'control_head'.
    - `has_new_entries(self)`: Determines whether there are new entries in a form.
    - `new_entries_total(self)`: Gets the total number of new entries in a form.
    - `last_submission_id(self)`: Retrieves the last submission ID for the specified form.
    - `has_valid_client(self)`: Checks if the JotForm client object is valid.

    Note:
    - This module requires the `APIKey` class to be defined.
    - The JotForm API requires a valid API key to make requests.
    - The `JotForm` class assumes that the `client` object has a method called `get_form` that returns information
        about the form specified by `form_id`.
    - The `JotForm` class relies on the `JotformAPIClient` class to interact with the JotForm API.

    Example usage:
    ```
    # Create an instance of the JotForm class
    jotform = JotForm(api_key='your_api_key', form_id='your_form_id')

    # Check if there are new entries in the form
    has_new_entries = jotform.has_new_entries

    # Get the total number of new entries in the form
    new_entries_total = jotform.new_entries_total

    # Get the last submission ID for the form
    last_submission_id = jotform.last_submission_id

    # Retrieve the new submissions for the form
    new_submissions = jotform.get_new_submissions()

    # Strip leading and trailing whitespace from an answer
    stripped_answer = jotform._strip_answer(answer)
    ```
    """
    DEFAULT_FORM_ID = None
    ILLEGAL_STARTING_CHARACTERS = ['<']
    IGNORED_FIELD_MESSAGE = "ignored due to illegal starting character"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, 'logger'):
            pass
        else:
            self.logger = kwargs.get('logger', getLogger('dummy_logger'))

        self._has_valid_client = False
        self._has_new_entries = None
        self._new_entries_total = None
        self._last_submission_id = None
        self._real_jf_field_names = None
        self._form_section_headers = None

        self.ignored_submission_fields = kwargs.get('ignored_submission_fields', [])

        self.form_id = kwargs.get('form_id', self.DEFAULT_FORM_ID)

        self._initialize_client()

        if not self.form_id and not self.DEFAULT_FORM_ID:
            raise AttributeError('form_id not found, if form_id was not a keyword arg, '
                                 'check that DEFAULT_FORM_ID is set in any subclasses.')

        if not self.has_valid_client:
            raise NoJotformClientError('no valid JotForm client object found.')
        else:
            self.logger.info(f"{self.__class__.__name__} Initialization complete.")

    @property
    def real_jf_field_names(self):
        """
        This code defines a property called `real_jf_field_names` in a class.

        The property returns a list of field names extracted from the answers of a JotForm submission. The field
        names are retrieved using the `get_answers_from_submission` method and stored in the `_real_jf_field_names`
        variable before being returned.

        If the `_real_jf_field_names` variable is not set, the code executes the `get_answers_from_submission` method
        and retrieves the field names from the last submission ID in the `new_entries_total` attribute.

        The property is accessed using dot notation on an instance of the class.

        """
        if not self._real_jf_field_names:
            self._real_jf_field_names = [x['field_name'] for x in self.get_answers_from_submission(
                self.new_entries_total['last_submission_id'])['answers']]
        return self._real_jf_field_names

    @property
    def form_section_headers(self):
        """
        This code defines a property method named 'form_section_headers'.

        When this property is accessed, it returns a list of field names from a submission's answers where the field
        type is 'control_head'. This property uses a lazy loading technique - it only retrieves the field names when
        the property is accessed for the first time and stores them in the '_form_section_headers' attribute for
        future use. If the '_form_section_headers' attribute is already populated, it simply returns its value
        without making additional database queries.

        """
        if not self._form_section_headers:
            self._form_section_headers = [x['field_name'] for x in
                                          self.get_answers_from_submission(
                                              self.new_entries_total['last_submission_id'])['answers']
                                          if x['field_type'] == 'control_head']
        return self._form_section_headers

    @property
    def has_new_entries(self):
        """
        This code defines a property called `has_new_entries` for a class.
        The property is used to determine whether there are new entries in a form.

        Attributes:
            - `client`: An object representing the client used to interact with forms.
            - `form_id`: The ID of the form to check for new entries.

        Returns:
            - `True` if there are new entries in the form.
            - `False` if there are no new entries in the form.

        Note:
        This property assumes that the `client` object has a method called `get_form` that returns information
        about the form specified by `form_id`. The information should include a field called 'new'
        representing the count of new entries.

        Usage:
        ```
        # Create an instance of the class
        client = Client()
        form_id = 123

        # Call the property to check for new entries
        is_new = client.has_new_entries
        ```
        """
        if int(self.client.get_form(self.form_id)['new']) > 0:
            self._has_new_entries = True
        else:
            self._has_new_entries = False
        return self._has_new_entries

    @property
    def new_entries_total(self):
        """
        @property
        def new_entries_total(self):
            """
        if self.has_new_entries:
            self._new_entries_total = {'total': int(self.client.get_form(self.form_id)['new']),
                                       'last_submission': self.client.get_form(self.form_id)['last_submission'],
                                       'last_submission_id': self.last_submission_id}
        else:
            self._new_entries_total = None
        return self._new_entries_total

    @property
    def last_submission_id(self):
        """
        Retrieves the last submission ID for the specified form.

        @return: The last submission ID as an integer.
        """
        self._last_submission_id = self._get_last_submission_id(self.client.get_form(self.form_id)['last_submission'])
        return self._last_submission_id

    @property
    def has_valid_client(self):
        if hasattr(self, 'client'):
            self._has_valid_client = True
        else:
            self._has_valid_client = False
        return self._has_valid_client

    @has_valid_client.setter
    def has_valid_client(self, value):
        self._has_valid_client = value

    def _initialize_client(self):
        if self.api_key:
            self.client = JotformAPIClient(self.api_key)
        else:
            self.client = JotformAPIClient(self._fetch_api_key(self.api_key_location))
        self._validate_client()

    def _validate_client(self):
        try:
            self.client.get_user()
            self.has_valid_client = True
        except HTTPError as e:
            raise JotFormAuthenticationError(
                url=e.url, code=e.code, msg=e.reason, hdrs=e.headers, fp=e.fp) from None

    def _get_last_submission_id(self, last_sub_datetime: Union[datetime, str]):
        """
        This method is used to get the last submission ID of a form based on the provided last submission datetime.

        Parameters:
        - last_sub_datetime: The last submission datetime to search for. It can be provided as a datetime object or a string in ISO format.

        Returns:
        - The last submission ID as an integer if it exists.
        - None if there is no submission matching the provided datetime.

        Note:
        - This method relies on the 'client' attribute which should be an instance of a client object that has the 'get_form_submissions' method.
        - The 'client.get_form_submissions' method returns a list of submissions for the provided form ID.
        - The method iterates through each submission and checks if the 'created_at' datetime matches the provided last submission datetime.
        - If a matching submission is found, its ID is stored in the 'last_sub_id' list.
        - The method returns the first ID from the 'last_sub_id' list if it is not empty.
        - If there are no matching submissions, None is returned.
        """
        last_sub_id = [x['id'] for x in self.client.get_form_submissions(self.form_id)
                       if datetime.fromisoformat(x['created_at']) == datetime.fromisoformat(last_sub_datetime)][0]
        if last_sub_id:
            return last_sub_id
        else:
            return None

    def get_new_submissions(self):
        """
        Returns the new submissions for a given form.

        This method retrieves new form submissions from the client based on the specified form ID. It filters the submissions to only return those with the 'new' attribute set to '1'.

        Returns:
            list: A list of new submissions, each represented as a dictionary.

                The dictionary contains attributes and their corresponding values for each submission.

                Example:
                {'id': 1, 'name': 'John Doe', 'age': 25, 'new': '1'}

                If no new submissions are found, it returns None.

            None: If no new submissions are found.
        """
        new_submissions = [x for x in self.client.get_form_submissions(self.form_id) if x['new'] == '1']
        if new_submissions:
            return new_submissions
        else:
            return None

    @staticmethod
    def _strip_answer(answer: Optional[Union[str, dict]]):
        if isinstance(answer, str):
            answer = answer.strip()
        elif isinstance(answer, dict) and 'datetime' in answer.keys():
            answer = answer['datetime']
        return answer

    def _get_answers_dict(self, raw_answers: dict):
        self.logger.warning("THIS IS MEANT TO BE OVERWRITTEN IN A SUBCLASS!")
        return raw_answers

    # noinspection PyTypeChecker
    def get_answers_from_submission(self, submission_id: str):
        self.logger.info(f"parsing submission_id: {submission_id}")

        submission_answers = {'submission_id': submission_id, 'answers': []}
        submission_json = dict(self.client.get_submission(submission_id)['answers'].items())

        for field in submission_json.keys():
            if field not in self.ignored_submission_fields:
                field_text = submission_json[field]['text']
                try:
                    # these would be other internal/title fields that can be ignored
                    if not self.is_illegal_field(field_text):
                        submission_answers['answers'].append(self._get_answers_dict(submission_json[field]))
                    else:
                        self.logger.debug(f'field {field_text} (aka \'{field}\') {self.IGNORED_FIELD_MESSAGE}')

                except KeyError:
                    self.logger.debug(f'no value found for: {field_text}')
                    submission_answers['answers'].append(self._get_answers_dict(submission_json[field]))

        return submission_answers

    def is_illegal_field(self, field_text: str) -> bool:
        return any([field_text.startswith(char) for char in self.ILLEGAL_STARTING_CHARACTERS])

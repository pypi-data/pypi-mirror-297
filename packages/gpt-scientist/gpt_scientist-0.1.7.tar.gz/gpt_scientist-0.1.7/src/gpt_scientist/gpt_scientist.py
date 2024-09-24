"""Main module."""

import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json
import tiktoken
import logging
from pydantic import create_model
from gpt_scientist.google_doc_parser import convert_to_markdown
from typing import Callable, Iterable

# Check if we are in Google Colab, and if so authenticate and import libraries to work with Google Sheets
try:
    from google.colab import auth
    IN_COLAB = True
    import gspread
    from google.auth import default
    from googleapiclient.discovery import build
    auth.authenticate_user()
except ImportError:
    IN_COLAB = False

# Princing for SOTA models in USD per 1M tokens at the time of writing
DEFAULT_PRICING = {
    'gpt-4o': {'input': 5, 'output': 15},
    'gpt-4o-2024-08-06': {'input': 2.5, 'output': 10},
    'gpt-4o-mini': {'input': 0.15, 'output': 0.6},
}

# Index of the first non-header row in google-sheet indexing
GSHEET_FIRST_ROW = 2

class Scientist:
    '''Configuration class for the GPT Scientist.'''
    def __init__(self, api_key: str = None):
        '''
            Initialize configuration parameters.
            If no API key is provided, the key is read from the .env file.
        '''
        if api_key:
            self._client = OpenAI(api_key=api_key)
        else:
            load_dotenv()
            self._client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = 'gpt-4o-mini' # Default model
        self.use_structured_outputs = True # Use structured outputs by default
        self.system_prompt = 'You are a social scientist analyzing textual data.' # Default system prompt
        self.num_results = 1 # How many completions to generate at once? The first valid completion will be used.
        self.num_reties = 10 # How many times to retry the request if no valid completion is generated?
        self.max_tokens = 2048 # Maximum number of tokens to generate
        self.top_p = 0.3 # Top p parameter for nucleus sampling (this value is quite low, preferring more deterministic completions)
        self.output_sheet = 'gpt_output' # Name (prefix) of the worksheet to save the output in Google Sheets
        self.pricing = DEFAULT_PRICING # Pricing for different models
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def set_model(self, model: str):
        '''Set the model to use for the GPT Scientist.'''
        self.model = model

    def set_use_structured_outputs(self, use_structured_outputs: bool):
        '''Set whether to use OpenAI's structured outputs feature to guarantee valid JSON responses.'''
        self.use_structured_outputs = use_structured_outputs

    def set_num_results(self, num_completions: int):
        '''Set the number of results to generate at once.'''
        self.num_results = num_completions

    def set_num_retries(self, num_retries: int):
        '''Set the number of retries if no valid completion is generated.'''
        self.num_reties = num_retries

    def set_system_prompt(self, system_prompt: str):
        '''Set the system prompt to use for the GPT Scientist.'''
        self.system_prompt = system_prompt

    def load_system_prompt_from_file(self, path: str):
        '''Load the system prompt from a file.'''
        with open(path, 'r') as f:
            self.system_prompt = f.read()

    def load_system_prompt_from_google_doc(self, doc_id: str):
        '''Load the system prompt from a Google Doc.'''
        if not IN_COLAB:
            self.logger.error("This method is only available in Google Colab.")
            return

        creds, _ = default()
        service = build('docs', 'v1', credentials=creds)
        doc = service.documents().get(documentId=doc_id).execute()
        self.system_prompt = convert_to_markdown(doc['body']['content'])

    def set_max_tokens(self, max_tokens: int):
        '''Set the maximum number of tokens to generate.'''
        self.max_tokens = max_tokens

    def set_top_p(self, top_p: float):
        '''Set the top p parameter for nucleus sampling.'''
        self.top_p = top_p

    def set_output_sheet(self, output_sheet: str):
        '''Set the name (prefix) of the worksheet to save the output in Google Sheets.'''
        self.output_sheet = output_sheet

    def set_pricing(self, pricing: dict):
        '''
            Add or update pricing information.
            Pricing table must be in the format {'model_name': {'input': input_cost, 'output': output_cost}},
            where input_cost and output_cost are the costs per 1M tokens.
        '''
        self.pricing = self.pricing | pricing

    def current_cost(self) -> dict:
        '''Return the cost corresponding to the current number of input and output tokens.'''
        price = self.pricing.get(self.model, {'input': 0, 'output': 0})
        input_cost = price['input'] * self._input_tokens / 1e6
        output_cost = price['output'] * self._output_tokens / 1e6
        return {'input': input_cost, 'output': output_cost}

    def _format_suffix(self, fields: list[str]) -> str:
        '''Suffix added to the prompt to explain the expected format of the response.'''
        return f"Your response must be a json object with the following fields: {', '.join(fields)}. The response must start with {{, not with ```json."

    def _create_prompt(self, user_prompt: str, input_fields: list[str], output_fields: list[str], row: pd.Series) -> str:
        prompt = f"{user_prompt}\n{self._input_fields_and_values(input_fields, row)}"
        if not self.use_structured_outputs:
            # If we are not using structured outputs, we need to add the description of the expected format to the prompt
            prompt = f"{prompt}\n{self._format_suffix(output_fields)}"
        return prompt

    def _prompt_model(self, prompt: str, output_fields: list[str]) -> dict:
        '''Send the prompt to the model and return the completions.'''
        if not self.use_structured_outputs:
            fn = self._client.chat.completions.create
            response_format={"type": "json_object"}
        else:
            fn = self._client.beta.chat.completions.parse
            response_format = create_model("Response", **{field: (str, ...) for field in output_fields})

        # Add input tokens to the total
        self._input_tokens += len(self._tokenizer.encode(prompt))
        messages = [{"role": "system", "content": self.system_prompt}] + self._examples + [{"role": "user", "content": prompt}]

        return fn(
                model=self.model,
                messages=messages,
                n=self.num_results,
                max_tokens=self.max_tokens,
                response_format=response_format,
                top_p=self.top_p,
            )

    def _parse_response(self, completion, output_fields: list[str]) -> dict:
        '''Parse model completion into a dictionary.'''
        if not self.use_structured_outputs:
            try:
                response = json.loads(completion.content.strip())
                # Check for missing fields unless we are using structured outputs
                missing_fields = [field for field in output_fields if field not in response]
                if missing_fields:
                    self.logger.warning(f"Response is missing fields {missing_fields}: {response}")
                    return None
                return response
            except json.JSONDecodeError as _:
                self.logger.warning(f"Not a valid JSON: {completion}")
                return None
        else:
            if completion.refusal:
                self.logger.warning(f"Completion was refused: {completion.refusal}")
                return None
            return completion.parsed.dict()

    def get_response(self, prompt: str, output_fields: list[str] = []) -> dict:
        '''
            Prompt the model until we get a valid json completion that contains all the output fields.
            Return None if no valid completion is generated after scientist.num_reties attempts.
        '''
        for attempt in range(self.num_reties):
            if attempt > 0:
                self.logger.warning(f"Attempt {attempt + 1}")

            try:
                completions = self._prompt_model(prompt, output_fields)

                # Add the content of all completions to the total output tokens
                self._output_tokens += sum([len(self._tokenizer.encode(completions.choices[i].message.content)) for i in range(self.num_results)])

                for i in range(self.num_results):
                    response = self._parse_response(completions.choices[i].message, output_fields)
                    if response is None:
                        continue
                    self.logger.debug(f"Response:\n{response}")
                    return response
            except Exception as e:
                self.logger.warning(f"Could not get a response from the model: {e}")

    def _input_fields_and_values(self, fields: list[str], row: pd.Series) -> str:
        '''Format the input fields and values for the prompt.'''
        return '\n\n'.join([f"{field}:\n```\n{row[field]}\n```" for field in fields])

    def _report_cost(self, input_tokens: int, output_tokens: int):
        cost = self.current_cost()
        self.logger.info(f"\tTotal cost so far: ${cost['input']:.4f} + ${cost['output']:.4f} = ${cost['input'] + cost['output']:.4f}    This row tokens: {input_tokens} + {output_tokens} ")

    def _add_example(self, prompt: str, row: pd.Series, input_fields: list[str], output_fields: list[str]):
        '''
            Create a few-shot example where the user message is the prompt and input fields form the given row,
            and the model response is the output fields of the row.
        '''
        # The input of the example is the full prompt as it would be sent to the model
        full_prompt = self._create_prompt(prompt, input_fields, output_fields, row)
        # The output of the example is a json object with the output fields of the row
        response = {field: row[field] for field in output_fields}
        self._examples.append({"role": "user", "content": full_prompt})
        self._examples.append({"role": "assistant", "content": json.dumps(response, ensure_ascii=False)})

    def analyze_data(self,
                     data: pd.DataFrame,
                     prompt: str,
                     input_fields: list[str],
                     output_fields: list[str],
                     write_output_row: Callable[[pd.DataFrame, int], None],
                     rows: Iterable[int],
                     examples: Iterable[int],
                     overwrite: bool,
                     row_index_offset: int = 0):
        '''
            Analyze all the `rows` in a pandas dataframe:
            for every value in the input_field column,
            send to the model the `prompt`, together with names and values of `input_fields`;
            parse `output_fields` from the response and write the current row into the dataframe.
            The dataframe is modified in place.
            `write_output_row` is a function used to save progress after every row (e.g. write to a spreadsheet where data came from).
            `examples` is a sequence of row indexes to be used as few-shot examples for the model;
            if `overwrite` is false, rows where any of the `output_fields` is non-empty will be skipped;
            `row_index_offset` is only used for progress reporting,
            to account for the fact that the user might see a non-zero based row indexing.
        '''
        # Check if all input fields are present in the dataframe
        for field in input_fields:
            if field not in data.columns:
                self.logger.error(f"Input field {field} not found.")
                return
        # If no input fields are specifies, use all columns except the output fields
        if not input_fields:
            input_fields = [field for field in data.columns if field not in output_fields]

        for field in output_fields:
            if field not in data.columns:
                # If the output field is not in the dataframe, add it
                data[field] = ''
            else:
                # Otherise, convert the field to string because the model will be returning strings
                # TODO: in the future, we may want to specify the type of the output fields
                data[field] = data[field].fillna('').astype(str)

        self._input_tokens, self._output_tokens = 0, 0
        self._tokenizer = tiktoken.encoding_for_model(self.model)
        if self.model not in self.pricing:
            self.logger.warning(f"No pricing available for {self.model}; cost will be reported as 0.")

        # Prepare the few-shot examples
        self._examples = []
        for i in examples:
            if i < 0 or i >= len(data):
                self.logger.error(f"Skipping example {i + row_index_offset} (no such row)")
                continue
            row = data.loc[i]
            self.logger.info(f"Adding example row {i + row_index_offset}")
            self._add_example(prompt, row, input_fields, output_fields)

        # Process every row in the given range
        for i in rows:
            if i < 0 or i >= len(data):
                self.logger.error(f"Skipping row {i + row_index_offset} (no such row)")
                continue

            row = data.loc[i]

            if not overwrite and any(row[field] for field in output_fields):
                # If any of the output fields is already filled, skip the row
                self.logger.info(f"Skipping row {i + row_index_offset} (already filled)")
                continue

            self.logger.info(f"Processing row {i + row_index_offset}")
            old_input_tokens, old_output_tokens = self._input_tokens, self._output_tokens
            full_prompt = self._create_prompt(prompt, input_fields, output_fields, row)
            response = self.get_response(full_prompt, output_fields)
            if response is None:
                self.logger.error(f"The model failed to generate a valid response for row: {i + row_index_offset}. Try again later?")
            else:
                for field in output_fields:
                    data.at[i, field] = response[field]
            write_output_row(data, i)
            self._report_cost(self._input_tokens - old_input_tokens, self._output_tokens - old_output_tokens)

    def analyze_csv(self,
                    path: str,
                    prompt: str,
                    input_fields: list[str] = [],
                    output_fields: list[str] = ['gpt_output'],
                    rows: Iterable[int] | None = None,
                    examples: Iterable[int] = [],
                    in_place: bool = True,
                    overwrite: bool = False):
        '''
            Analyze a CSV file.
            If in_place is True, save the results to the input file, otherwise create a unique output file.
        '''
        # Create a unique output file name based on current time;
        # when in_place is True, this file only serves as a backup, in case the finally block fails to run
        out_file_name = os.path.splitext(path)[0] + f'_output_{pd.Timestamp.now().strftime("%Y%m%d%H%M%S")}.csv'

        def write_output_row(data, i):
            # Append the row to the output file
            data.loc[[i]].to_csv(out_file_name, mode='a', header=(i == 0), index=False)

        data = pd.read_csv(path)
        if rows is None:
            rows = range(len(data))
        try:
            self.analyze_data(data, prompt, input_fields, output_fields, write_output_row, rows, examples, overwrite)
        except Exception as _:
            pass
        finally:
            if in_place and os.path.exists(out_file_name):
                data.to_csv(path, index=False)
                os.remove(out_file_name)

    def _parse_row_ranges(self, range_str: str, n_rows: int) -> list[int]:
        '''
            Parse a g-sheet-style row range string (e.g., "2:10,12,15:") into a list of row indexes.
            Note that g-sheet ranges are effectively 2-based, because the first row is the header,
            and the result is 0-based.
        '''
        row_indexes = []
        ranges = range_str.split(',')

        def parse_int(s):
            try:
                return int(s)
            except ValueError:
                self.logger.error(f"Invalid row range: {range_str}")
                return GSHEET_FIRST_ROW

        for r in ranges:
            if ':' in r:  # Range like 1:10, 2:, or :
                parts = r.split(':')
                if len(parts[0]) == 0:
                    start = 0
                else:
                    start = parse_int(parts[0]) - GSHEET_FIRST_ROW
                if len(parts[1]) == 0:
                    end = n_rows
                else:
                    end = parse_int(parts[1]) - GSHEET_FIRST_ROW + 1
                row_indexes.extend(range(start, end))
            elif r:  # Single row like 1
                row_indexes.append(parse_int(r) - GSHEET_FIRST_ROW)

        return row_indexes

    def _output_sheet_name(self, spreadsheet) -> str:
        '''Create a new worksheet in the spreadsheet to save the output, avoiding name conflicts.'''
        worksheet_list = spreadsheet.worksheets()
        worksheet_names = [worksheet.title for worksheet in worksheet_list]
        if self.output_sheet in worksheet_names:
            i = 1
            while f"{self.output_sheet}_{i}" in worksheet_names:
                i += 1
            return f"{self.output_sheet}_{i}"
        else:
            return self.output_sheet

    def _convert_value_for_gsheet(self, val):
        '''Convert complex types to strings for Google Sheets.'''
        if isinstance(val, list):
            return ', '.join(map(str, val))  # Convert list to comma-separated string
        elif isinstance(val, dict):
            return str(val)  # Convert dictionary to string
        else:
            return val  # Leave supported types as-is

    def analyze_google_sheet(self,
                             sheet_key: str,
                             prompt: str,
                             input_fields: list[str] = [],
                             output_fields: list[str] = ['gpt_output'],
                             rows: str = ':',
                             examples: str = '',
                             in_place: bool = True,
                             overwrite: bool = False,
                             worksheet_index: int = 0):
        '''
            When in Colab: analyze data in the Google Sheet with key `sheet_key`; the user must have write access to the sheet.
            Use `worksheet_index` to specify a sheet other than the first one.
            If `in_place` is True, the input sheet will be extended with the output data; otherwise a new sheet will be created.
            If `n_rows` is provided, only the first n_rows are processed (useful for testing).
        '''
        if not IN_COLAB:
            self.logger.error("This method is only available in Google Colab.")
            return
        creds, _ = default()
        gc = gspread.authorize(creds)

        # Open the spreadsheet and the worksheet, and read the data
        spreadsheet = gc.open_by_key(sheet_key)
        worksheet = spreadsheet.get_worksheet(worksheet_index)
        data = worksheet.get_all_records()
        data = pd.DataFrame(data)

        # If in_place is False, create a copy of the worksheet
        if not in_place:
            worksheet = worksheet.duplicate(new_sheet_name=self._output_sheet_name(spreadsheet), insert_sheet_index=worksheet_index+1)

        # Prepare the worksheet for output and get output column indices
        header = worksheet.row_values(1)
        output_column_indices = []

        for field in output_fields:
            if field in header:
                # If the column exists, get its index (1-based)
                output_column_indices.append(header.index(field) + 1)
            else:
                if len(header) + 1 > worksheet.col_count:
                    # Add more columns if necessary
                    worksheet.add_cols(1)
                # If the column doesn't exist, append it to the header
                worksheet.update_cell(1, len(header) + 1, field)  # Add to the next available column
                output_column_indices.append(len(header) + 1)
                header.append(field)  # Update the header list

        # Now we have the column indices, prepare the function that outputs a row
        def write_output_row(data, i):
            for idx, field in enumerate(output_fields):
                col_index = output_column_indices[idx]
                worksheet.update_cell(i + GSHEET_FIRST_ROW, col_index, self._convert_value_for_gsheet(data.at[i, field]))

        self.analyze_data(data,
                          prompt,
                          input_fields,
                          output_fields,
                          write_output_row,
                          self._parse_row_ranges(rows, len(data)),
                          self._parse_row_ranges(examples, len(data)),
                          overwrite,
                          row_index_offset=GSHEET_FIRST_ROW)

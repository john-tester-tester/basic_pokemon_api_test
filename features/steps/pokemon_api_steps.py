import os

import requests
from behave import *


@given('a base URL "{common_url_string}"')
def given_a_base_url_has_been_provide(context, common_url_string):
    context.url = str(common_url_string).strip()


@given('the base URL is valid')
def given_a_url_user_option_has_been_provide(context):
    assert (context.url.startswith(r"http://") or
            context.url.startswith(r"https://")), f"Error: {context.url} does not begin with 'http://' or 'https://'"


@given('this api option "{api_option_string}"')
def given_a_url_user_option_has_been_provide(context, api_option_string):
    context.url = context.url + str(api_option_string).strip()


@when('the user GET request is sent')
def send_url_get_request(context):
    try:
        context.result = requests.get(context.url)
    except Exception as e:
        print(e)
        assert False, f"Error: problem with performing a get request, url sent \"{context.url}\""


@then('we should receive a "{response_value}" response')
def check_response_value(context, response_value):
    assert context.result.status_code == int(response_value), f"Error: incorrect response value, expected {response_value},actual value {context.result.status_code}"


@then('response should match values in this expected file "{expected_result_file}" and "{expected_number_of_results}" apis are returned')
def check_json_response_should_match_values_in_the_expected_file(context, expected_result_file, expected_number_of_results):
    json_response = return_json_data_from_api_response(context)

    if not (os.path.exists(expected_result_file)):
        current_path = os.getcwd()
        assert False, f"Error: File not found, current path {current_path}, expected {expected_result_file}"
    else:
        with open(expected_result_file, "r") as import_file:
            lines = import_file.readlines()
            number_of_fields = 0
            for expected_item, (actual_value, actual_path) in zip(lines, json_response.items()):
                    expected_value, expected_path = str(expected_item).split('\t')
                    expected_value = str(expected_value).strip().replace('"','')
                    expected_path = str(expected_path).strip().replace('"','')
                    assert expected_value == actual_value, f"Error: expected value {expected_value}, actual value {actual_value}"
                    assert expected_path == actual_path, f"Error: expected path {expected_path}, actual path {actual_path}"
                    number_of_fields += 1

            assert number_of_fields == int(
                expected_number_of_results), (f"Error: incorrect number of apis returned {expected_number_of_results}, "
                                              f"actual number returned {number_of_fields}")


@then('the following data is returned')
def check_json_response_should_match_values_in_the_table(context):
    context.number_of_fields_returned = 0
    json_response = return_json_data_from_api_response(context)
    expected_values = {}
    actual_keys =[]

    for row in context.table:
        expected_values.update({row['Field']: row['Value']})

    for actual_key, actual_value in json_response.items():

        context.number_of_fields_returned +=1

        if actual_key in expected_values.keys():
            assert expected_values[actual_key] == str(actual_value), (f"Error: expected value {expected_values[actual_key]}, "
                                                                      f"actual value {actual_value}")
            actual_keys.append(actual_key)

    sorted_actual_keys = sorted(actual_keys)
    sorted_expected_keys = sorted(expected_values.keys())
    assert sorted_expected_keys == sorted_actual_keys, (f"Error: expected field names {sorted_expected_keys}, "
                                                                           f"actual field names {sorted_actual_keys}")


@then('"{expected_number_of_fields}" fields are present in the data')
def check_json_response_contains_the_correct_number_of_fields(context, expected_number_of_fields):
    assert expected_number_of_fields == str(context.number_of_fields_returned), (f"Error: expected number of fields {expected_number_of_fields}, "

                                                                                 f"actual number of fields {context.number_of_fields_returned}")
def return_json_data_from_api_response(context):
    try:
        return context.result.json()
    except Exception as e:
        print(e)
        assert False, f"Error: unable to extract json data from the API response"


if __name__ == '__main__':
    from behave import __main__ as behave_executable
    # adjust this directory base on which folder this project has been placed in.
    #so in this case I place my git projects in C:\Dev_git_projects
    os.chdir(r'C:\Dev_git_projects\basic_pokemon_api_test\features')
    behave_executable.main(None)
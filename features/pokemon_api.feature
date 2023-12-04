Feature: Pokemon api

  Background: Set base URL
    Given a base URL "https://pokeapi.co/api/v2"

# I found one duplication in this document page https://pokeapi.co/docs/v2
# for example, location area appears in
# https://pokeapi.co/docs/v2#locations-section and https://pokeapi.co/docs/v2#pokemon-section
# the api tested below does not have duplicates, so, the number of tests may differ between this test
# and document page https://pokeapi.co/docs/v2
  Scenario: Check the content and the number of api methods available
    Given the base URL is valid
    When the user GET request is sent
    Then we should receive a "200" response
    And response should match values in this expected file "expected_API_Results.txt" and "48" apis are returned

  Scenario: Check an invalid rest api request, "test", expect an error to be returned
    Given this api option "/test"
    When the user GET request is sent
    Then we should receive a "404" response

  Scenario: Check a popular pokemon character, Charizard, can be retrieved
    Given this api option "/pokemon/charizard"
    When the user GET request is sent
    Then we should receive a "200" response
    And the following data is returned
      | Field           | Value     |
      | base_experience | 267       |
      | name            | charizard |
      | weight          | 905       |
    And "19" fields are present in the data

  # this scenario will fail, count returned is 1292
  # but after some experiments it appears the maximum
  # number is 1275
  Scenario: Check the number of pokemons
    Given this api option "/pokemon"
    When the user GET request is sent
    Then we should receive a "200" response
    And the following data is returned
      | Field | Value |
      | count | 1275  |

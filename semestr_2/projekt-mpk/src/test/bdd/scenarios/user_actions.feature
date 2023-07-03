# Created by lisik at 02/07/2023
Feature: User actions # Enter feature name here
  # Enter feature description here

  Scenario: User creates an account
    Given app is running
    When User creates account with test@test.com mail secret_pass password test name
    Then User with mail test@test.com and password secret_pass is persisted in repository
    Then User receives cookie

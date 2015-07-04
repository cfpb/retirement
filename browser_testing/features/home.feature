Feature: verify the Home page works according to requirements
As a first time visitor to the Retirement page
I want to navigate the home page
So that I can find the information I'm looking for

Background:
   Given I navigate to the Retirement landing page

@smoke_testing @landing_page
Scenario: Testing landing page
  Then I should see "Consumer Financial Protection Bureau" displayed in the page title

@smoke_testing @landing_page
Scenario Outline: Select month and day and year and income
  When I enter month "<month>"
  And I enter day "<day>"
  And I enter year "<year>"
  And I enter income "<income>"
  And I click get estimate
  Then I should see result "<expected_result>" displayed in graph-container-text

Examples:
  | month | day | year | income |  expected_result
  | 7     | 7   | 1970 | 70000  |  67

@smoke_testing @landing_page
Scenario: Select age
  When I Choose age "70"
  Then I should see "70" displayed in age_selector_response

@smoke_testing @landing_page
Scenario Outline: Test links in the landing page
   Given I navigate to the Retirement Landing page
   When I click on the "<link_name>" link
   Then I should see the "<full_url>" URL with page title "<page_title>"

Examples:
  | link_name                           | page_title               | full_url                             |
  | Learn how estimates are calculated. | Quick Calculator FAQs    | www.ssa.gov/OACT/quickcalc/faqs.html |

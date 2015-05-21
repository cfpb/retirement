Feature: verify the navigation tabs/links works according to requirements
  As a first time visitor to the Retirement page
  I want to click on invidual tabs and links
  So that I can easily navigate the site


@smoke_testing @landing_page
Scenario Outline: Test links in the landing page
   Given I navigate to the Retirement Landing page
   When I click on the "<link_name>" link
   Then I should see the "<relative_url>" URL with page title "<page_title>"

Examples:
  | link_name                                       | page_title               | relative_url                     |
  | Learn how estimates are calculated.             | /somelink                | /                                |

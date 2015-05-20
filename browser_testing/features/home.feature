Feature: verify the Home page works according to requirements
As a first time visitor to the Owning a Home page
I want to navigate the home page
So that I can find the information I'm looking for

Background:
   Given I navigate to the Retirement Landing page

@smoke_testing @landing_page
Scenario: Testing landing page
  Then I should see "Consumer Financial Protection Bureau" displayed in the page title

@smoke_testing @landing_page
Scenario: Select age
  When I Choose age "64"
  Then I should see "Consumer Financial Protection Bureau" displayed in the page title
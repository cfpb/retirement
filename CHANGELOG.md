Notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.

## Unreleased
- 

## 0.4.7
- Added lifetime calculations to api and removed from js
- Deleted unneeded grunt packages
- Added `.npmrc` and `npm-shrinkwrap.json` files
- Removed redundant cf-icon CSS code

## 0.4.62
- Changed the url namespace for the 'about' page to be specific to retirement

## 0.4.61
- Blanked out `about` page content pending clearance
- Switched to `merge=union` for CHANGELOG.md in .gitattributes
- Fixed 'claiming at 68' phrasing error
- Fixed handling of birth dates on the first of a month
- Fixed error message for ages over 70
- Translated date placeholders and explanatory text for folks past FRA
- Added urls, view and empty templates for 'about' pages in English and Spanish
- Added 'about' page content
- Fixed additional claiming phrasing errors
- Removed final references to raphael-min.js and fixed spinner direction
- Replaced custom slider with a standard range input
- Switched to a CFPB common navigation header
- Updated hero treatment and page spacing
- Added toggle link to switch between languages
- Added Calibration model to support SSA value checks
- Added ssa_check.py utility for monitoring SSA Quick Calculator values

## 0.4.58
- switch back to ssa.gov for our requests, after SSA started redirecting calls to socialsecurity.gov

## 0.4.57
- fix tests should they happen to run on leap day (Edgehog Day)

## 0.4.56
- fix prorating in edge cases

## 0.4.53
- fixed handling of edge case: display of age-62 graph bar when birth date = 1/2/1952

## 0.4.52
- fixed outdated myRa link, English and Spanish

## 0.4.51
- fixed English and Spanish page titles to avoid using nonstandard pipe character

## 0.4.5
- Added switch for question graphics with English text on Spanish implementation

## 0.4.4
- fix for production speed issue
- adds navigation to match rest of site
- New wording order for hero
- Fix to graph explainer line ('Select claiming ages ...')
- Redirect for `/jubilacion/` (not in this repo, but in this release)
- Fix for api checker (randomizes parameters to avoid cache hits)
- Hero cactus shadow fixed

## 0.4.3
- hotfixes to fix Spanish content for testing

## 0.4.1
- hotfix for SSA's change to https

## 0.4.0
- completed Spanish implementation for user testing, adding translations for error messaging and javascript content
- bumped app's timeout to avoid caching of occasional slow SSA responses
- added front-end build script and setup.py code to invoke it (not used yet in deployments)
- added redirect to app's url config so it doesn't need to be handled in apache

## 0.3.0
- added a tooltip for those who claim early but keep working, in the 'sixties' question
- major overhaul to front-end code to integrate grunt tasks and npm
- addition of mocha tests and 'npm test' command

## 0.2.0
- changed title and `h1` to **Before you claim**
- made content changes based on user testing, including hiding the graph initially
- fixed mobile alignment of graph elements
- changed final url field to reflect new title

## 0.1.7
**2015-07-15**

#### Fixed
- hotfix to make tool tips work in IE versions

## 0.1.5
**2015-07-14**

#### Fixed
- mobile breakpoints for bar graph

## 0.1.4
**2015-07-14**

#### Fixed
- Bugs and content issues for user testing

## 0.1.3
**2015-07-08 – soft launch for user testing**

#### Fixed
- Static pathing for live site

## 0.1.2
**2015-07-08**

#### Fixed
- Views for mobile devices

## 0.1.1
**2015-07-07**

#### Added
- table migrations for models

## 0.1.0
**2015-07-07 – release to prep for deployment**

#### Added
- Initial working graph, questions and interactions

## 0.0.1
**2015-04-06**

#### Added
- Initial endpoints

#### Deprecated
- Nothing

#### Removed
- Nothing

#### Fixed
- Nothing.


# Before You Claim - Front-end Documentation

This document is intended to serve as a supplement to comments found in the
code and README.md to further explain the front-end, including choices, MVW
framework, etc.

__This document is current as of 4/28/2016.__

## Contributing Developers

This document currently refers to front-end work done by:
* Bill Higgins (@higs4281)
* Chuck Werner (@mistergone)
* Marteki Reed (@marteki)
* Nicholas Johnson (@niqjohnson)

## Following the CFPB Front-End Standards

This front-end attempts to follow the [CFPB Front-End
Standards](https://github.com/cfpb/front-end) wherever possible and
applicable.

## The MVW framework

The front end code is organized into a framework we call __Model-View-
Wizard__, which is a variation of the common MVC framework in which
"Controllers" are called "Wizards" because the term "Controller" is both
misleading and less fun.

### index.js

The `src/index.js` file initializes the application by initializing all the
views. More information about initializing the views can be found in each
individual view's JS file.

### The Models

As of `0.6.2` (7/12/2018), there are two models in the front-end:

* __(Monthly) Benefits Model__ (`src/models/benefits-model.js`) - This model
contains the monthly benefit of the user at any given retirement age, based on
their date of birth (DOB) and income input. The data that fills this model
comes from our API endpoint, i.e. the backend of this application.

* __Lifetime Benefits Model__ (`src/models/lifetime-model.js`) - This model
contains the lifetime benefit of the user at any given retirement age, based
on their date of birth (DOB) and income input. The data that fills this model
comes from our API endpoint, i.e. the backend of this application. While it
might seem that the lifetime benefit is easily calculated by multiplying the
monthly benefit, we found enough cases of complexity to justify these values
being calculated in the backend and passed along as well.

### The Views

As of `0.6.2` (7/12/2018), there are four views in the front-end:

* __Graph View__ (`src/views/graph-view.js`) - This view does a majority of the
work on the page, since the most complexity exists in the display of the graph
elements and their interactions. More information is available in the JSDoc
comments for the individual functions inside this view.

* __Next Steps View__ (`src/views/next-steps-view.js`) - This view handles the
feedback form and such at the bottom of the form.

* __Questions View__ (`src/views/questions-view.js`) - This view handles the
questions in Step 2, including ensuring the user sees the appropriate
responses based on their age. More information is available in the JSDoc
comments for the individual functions inside this view.

* __tooltips__ (`src/views/tooltips-view.js`) - Lacking a standard package for
tooltips, this view provides the code necessary for the tooltips found
throughout the page.

### The Wizards

As of `0.6.2` (7/12/2018), there are three wizards in the front-end:

* __Fetch API Data__ (`/src/wizards/fetch-api-data.js`) - This wizard handles
the interaction when a user uses the graph view's form to request Social
Security Benefits data from our backend. It is a fairly simple AJAX request,
but note that it returns a promise. This promise is used by the graph view to
determine when to display the incoming data.

* __Get Model Values__ (`/src/wizards/get-model-values.js`) - As always, the
views want that precious data from the models, and this is the standard
helper. This wizard returns objects based on the model data requested.

* __Update Model__ (`src/wizards/update-model.js`) - Inevitably, the view wants
to send data back to the models. This wizard does just that - it has two main
functions to update each of the two models, as well as a function that
interprets the API data into data the models and views can use.

### The Utilities

This front-end also includes some utility files, which are generally self-
contained functions that are used by the views and models. These utilities are
generally akin to npm packages, but haven't quite made the jump to primetime
yet.

As of `0.6.2` (7/12/2018), there are five utilities in the front-end:

* __Enforce Range__ (`/src/utils/enforce-range.js`) - This is a very simple
utility that ensures a number falls within a range, and changes the number to
the max or min value if it falls outside that range. It's very useful for
`valid-dates.js`.

* __Handle String Input__ (`/src/utils/handle-string-input.js`) - This is
hopefully a more elegant way to take in a string and interpet the number
intended by the user than alternatives like `parseInt`. It tries hard to
determine decimal placement and whether the intended Number is negative.

* __Is element in View__ (`/src/utils/is-element-in-view.js`) - Returns true
or false on the question of whether an element is in the user's browser view.

* __Number to Money__ (`/src/utils/num-to-money.js`) - A simple function that
takes a number and formats it into a currency String.

* __Valid Dates__ (`/src/utils/valid-dates.js`) - A function that determines
whether a given date combination is valid. Dates of birth are validated
before they're sent off to the API.


## gettext and Translation

The application makes use of `gettext()`, a function created by Django
for use in JavaScript to retrieve translations of text elements.
This function is called as `window.gettext` and doesn't really
interact with the rest of the front-end,
instead simply providing translated strings in places.

## Graph and visualization choices

Originally, this application used the Raphael graphics library to provide
SVGs and support for older browsers which do not render SVGs. However, Raphael
was much more complexity than was required.

Since all but one of the shapes in the graph are simple rectangles,
we decided to remove Raphael and instead use styled HTML elements.
This gave us the distinct advantage of complete functionality
in older browsers as well as easy fidelity in mobile browsers.

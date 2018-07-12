import graphView from './views/graph-view';
import questionsView from './views/questions-view';
import nextStepsView from './views/next-steps-view';
import tooltipsView from './views/tooltips-view';

// TODO: remove jquery.
import $ from 'jquery';

const app = {
  init: function() {
    graphView.init();
    questionsView.init();
    nextStepsView.init();
    tooltipsView.init();
  }
};

$( document ).ready( function() {
  app.init();
} );

import benefitsModel from '../models/benefits-model';
import lifetimeModel from '../models/lifetime-model';

// TODO: remove jquery.
import $ from 'jquery';

const update = {

  /**
   * This function updates properties of the benefits model
   * @param {string} prop         The property to be updated
   * @param {number|string} val   The new value of the property
   */
  benefits: function( prop, val ) {
    benefitsModel.values[prop] = val;
  },
  lifetime: function( prop, val ) {
    lifetimeModel.values[prop] = val;
  },

  /**
   * This function takes a response from an AJAX call and processes
   * the response into the benefits model.
   * @param {object} resp   The AJAX response object
   */
  processApiData: function( resp ) {
    const data = resp.data;
    let fullAge = Number( data['full retirement age'].substr( 0, 2 ) );
    if ( resp.currentAge > fullAge ) {
      fullAge = resp.currentAge;
    }
    $.each( resp.data.benefits, function( i, val ) {
      if ( i.substr( 0, 3 ) === 'age' ) {
        const prop = i.replace( ' ', '' );
        update.benefits( prop, val );
      }
    } );
    $.each( resp.data.lifetime, function( prop, val ) {
      update.lifetime( prop, val );
    } );
    update.benefits( 'currentAge', resp.current_age );
    update.benefits( 'past_fra', resp.past_fra );
    update.benefits( 'fullRetirementAge', data['full retirement age'] );
    update.benefits( 'earlyRetirementAge', data['early retirement age'] );
    update.benefits( 'fullAge', fullAge );
    update.benefits( 'earlyAge', Number( data['early retirement age']
      .substr( 0, 2 ) ) );
    update.benefits(
      'monthsPastBirthday',
      Number( data.months_past_birthday )
    );
  }

};

module.exports = update;

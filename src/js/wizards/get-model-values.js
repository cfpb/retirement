import benefitsModel from '../models/benefits-model';
import lifetimeModel from '../models/lifetime-model';

const getModel = {
  benefits: () => benefitsModel.values,
  lifetime: () => lifetimeModel.values
};

module.exports = getModel;

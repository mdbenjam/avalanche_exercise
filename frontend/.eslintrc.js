const { Neutrino } = require('neutrino');

module.exports = Neutrino({ root: __dirname })
  .use('.neutrinorc.js', {
    eslint: {
      failOnError: false
    }
  })
  .call('eslintrc');

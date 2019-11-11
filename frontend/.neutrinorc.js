module.exports = {
  use: [
    '@neutrinojs/airbnb',
    [
      '@neutrinojs/react',
      {
        html: {
          title: 'frontend'
        },
        devServer: {
          allowedHosts: [
            'frontend'
          ]
        }
      }
    ],
    '@neutrinojs/jest'
  ]
};

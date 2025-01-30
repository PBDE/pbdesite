
const path = require('path');

module.exports = {
//   entry: './legion.js',  // path to our input file
  entry: path.resolve(__dirname, 'javascript') + '/legion.js',
  output: {
    filename: 'legion-bundle.js',  // output bundle file name
    path: path.resolve(__dirname, './static/legion/javascript'),  // path to our Django static directory
  },
};
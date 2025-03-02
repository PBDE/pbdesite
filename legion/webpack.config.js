
const path = require('path');

module.exports = {
  entry: path.resolve(__dirname, 'javascript') + '/legion.js',
  output: {
    filename: 'legion-bundle.js',  
    path: path.resolve(__dirname, './static/legion/javascript'),
  },
};
// webpack.config.js

const path = require('path');
const nodeExternals = require('webpack-node-externals');

module.exports = {
  entry: {
    extension: './extension.js', // Update this path to your main JS file
  },
  target: 'node',
  externals: [
    nodeExternals(),
    {
      vscode: 'commonjs vscode' // Add this line
    }
  ],
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'extension.js',
    libraryTarget: 'commonjs2',
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader', // Optional: If using Babel
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js'],
  },
};

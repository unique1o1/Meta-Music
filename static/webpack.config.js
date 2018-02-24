const webpack = require("webpack");

const config = {
  entry: __dirname + "/js/index.js",

  output: {
    path: __dirname + "/dist",
    filename: "bundle.js"
  },
  resolve: {
    extensions: [".js", ".jsx"]
  },
  module: {
    rules: [
      {
        test: /\.js?/,
        exclude: /node_modules/,
        use: "babel-loader"
      }
    ]
  }
};

module.exports = config;

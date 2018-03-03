const webpack = require("webpack");

const config = {
  entry: [
    __dirname + "/js/index.js",
    __dirname + "/js/app.js",
    __dirname + "/js/card.js",
    __dirname + "/js/bootstrap.min.js",

    __dirname + "/js/jquery-3.3.1.min.js"
  ],

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

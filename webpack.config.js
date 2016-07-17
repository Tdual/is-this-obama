module.exports = {
  entry: __dirname + "/static/js/src/app.js",
  output: {
    path: __dirname + '/static/js/',
    filename: 'index.js'
  },
  module: {
    loaders: [
      {
        test: /\.js[x]?$/,
        exclude: /node_modules/,
        loader: "babel",
        query:{
          presets: ['react', 'es2015']
        }
      }
    ]
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  }
};

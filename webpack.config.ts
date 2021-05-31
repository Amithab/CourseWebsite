import HtmlWebpackPlugin from 'html-webpack-plugin';
import path from "path";
import * as webpack from 'webpack';

const config: webpack.Configuration = {
  entry: "./src/index.tsx",
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: ["style-loader", "css-loader", "sass-loader"] // loaded right to left, css-loader loads the actual file, while style loader injects the styles
      },
      {
        test: /\.css$/,
        use: ["style-loader", {loader: "css-loader", options: { modules: {localIdentName: '[path][name]__[local]'}}}]
      },
      /*{
        test: /\.css$/,
        use: ["style-loader", {
          loader: "typings-for-css-modules-loader",
          options: {
            modules: true,
            namedExport: true,
            camelCase: true
          }
        }]
      },*/
      {
        test: /\.js$/,
        use: ["babel-loader"],
      },
      {
        test: /\.tsx?$/,
        use: ["ts-loader"],
        exclude: /node_modules/,
      },
      {
        test: /\.svg/,
        type: 'asset/resource'
      }
    ]
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  optimization: {
    splitChunks: { chunks: "all" }
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, "src", "index.html")
    })
  ],
  devtool: "source-map",
  devServer: {
    historyApiFallback: true, // Can change url to work with react router
  },
};

export default config;

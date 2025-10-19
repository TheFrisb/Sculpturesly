// webpack.config.js
const path = require('path');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = (env, argv) => {
  const isProd = argv.mode === 'production';

  return {
    context: path.resolve(__dirname),
    entry: {
      main: './src/index.js'
    },
    output: {
      path: path.resolve(__dirname, 'static/js/webpack-bundles'),
      filename: '[name].[contenthash].js'
    },
    mode: isProd ? 'production' : 'development',
    devtool: isProd ? false : 'eval-cheap-module-source-map',
    module: {
      rules: [
        {
          test: /\.m?js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader'
          }
        }
      ]
    },
    plugins: [
      new CleanWebpackPlugin(),
      new BundleTracker({filename: './webpack-stats.json'})
    ],
    optimization: {
      minimize: isProd,
      minimizer: [
        new TerserPlugin({
          terserOptions: {
            compress: {
              drop_console: true,
              pure_funcs: ['console.info', 'console.debug', 'console.warn']
            },
            format: {comments: false}
          },
          extractComments: false
        })
      ],
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendors: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all'
          }
        }
      },
      runtimeChunk: 'single',
      moduleIds: 'deterministic'
    },
    performance: {
      hints: isProd ? 'warning' : false
    },
    stats: {
      children: false
    }
  };
};

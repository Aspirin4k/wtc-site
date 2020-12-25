const path = require('path');

const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

module.exports = {
    entry: [path.resolve(__dirname, '../src/index.js')],
    output: {
        filename: '[name].[contenthash].js',
        path: path.resolve(__dirname, '../dist/static'),
        publicPath: '/'
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    mode: 'production',
    plugins: [
        new CleanWebpackPlugin({
            verbose: true
        }),
        new WebpackManifestPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    "style-loader",
                    "css-loader",
                    "sass-loader",
                ],
            }
        ]
    }
};
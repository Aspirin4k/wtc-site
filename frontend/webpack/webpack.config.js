const path = require('path');

const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    entry: path.resolve(__dirname, '../src/index.js'),
    output: {
        filename: 'build.js',
        path: path.resolve(__dirname, '../../static/app'),
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    mode: 'production',
    plugins: [
        new CleanWebpackPlugin({
            verbose: true
        }),
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
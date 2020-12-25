const path = require('path');

const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

module.exports = {
    entry: path.resolve(__dirname, '../src/index.js'),
    output: {
        filename: 'build.js',
        path: path.resolve(__dirname, '../dist-dev/static'),
        publicPath: '/'
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    mode: 'development',
    devtool: 'inline-source-map',
    plugins: [
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
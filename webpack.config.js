const path = require('path');
const HTMLWebpackPlugin = require('html-webpack-plugin');
const MiniCSSExtractPlugin = require('mini-css-extract-plugin');
const development = process.env.NODE_ENV === 'development';

module.exports = {
    entry: './client/index.js',
    output: {
        path: development ? path.resolve('client/build') : path.resolve('client/dist'),
        filename: 'main.js'
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                test: /\.scss$/,
                use: [
                    development ? 'style-loader' : MiniCSSExtractPlugin.loader,
                    'css-loader',
                    'sass-loader',
                    'postcss-loader'
                ]
            },
            {
                test: /\.(png|svg|jpg|gif|ico)$/,
                use: 'file-loader'
            }
        ]
    },
    plugins: [
        new MiniCSSExtractPlugin({
            filename: '[name].css',
            chunkFilename: '[id].css',
        }),
        new HTMLWebpackPlugin({
            template: './client/public/index.html',
            filename: './index.html'
        })
    ]
};
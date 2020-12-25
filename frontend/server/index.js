import React from 'react';
import express from 'express';
import fs from 'fs';
import path from 'path';
import { Proxy } from 'axios-express-proxy';
import { renderToString } from 'react-dom/server';

import config from '../config/env.json';
import { App } from '../src/App';
import { request } from './api';

const app = express();
const port = config.port;

app.set('view engine', 'ejs');
app.set('views', path.resolve(__dirname, 'views'));
app.use(express.static(path.resolve(__dirname, 'static')));

if (DEV) {
    const webpack = require('webpack');
    const webpackDevMiddleware = require('webpack-dev-middleware');
    const webpackHotMiddleware = require('webpack-hot-middleware');
    const webpackConfig = require('../webpack/webpack.config.dev');
    const compiler = webpack(webpackConfig);

    app.use(
        webpackDevMiddleware(compiler, {
            publicPath: webpackConfig.output.publicPath,
            writeToDisk: true
        })
    );

    app.use(
        webpackHotMiddleware(compiler, {
            log: console.log
        })
    );
}

let manifest = null;
app.get(['/', '/page/:num'], (req, res) => {
    return request( req.params.num || 0).then((response) => {
        if (null === manifest) {
            manifest = JSON.parse(fs.readFileSync(path.resolve(__dirname, 'static/manifest.json')));
        }

        const { data } = response;
        const { titles, number_of_pages } = data;
        const content = renderToString(<App payload={data} />);
        return res.render('index', {content, titles, number_of_pages, manifest});
    })
});
app.get('*', (req, res) => {
    return Proxy(config.api + req.url, req, res);
});

app.listen(port, () => {
    console.log(`Started server on port ${port}`);
});
import axios from 'axios';

import config from '../config/env.json';

export const request = (pageNum) => {
    return axios.get(`${config.api}/page/${pageNum}`);
};
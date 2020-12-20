import React from 'react';
import ReactDOM from 'react-dom';

import { App } from "./App";
import './index.scss';

const wrapper = document.getElementById('application');
wrapper && serverPayload && ReactDOM.render(<App payload={serverPayload} />, wrapper);
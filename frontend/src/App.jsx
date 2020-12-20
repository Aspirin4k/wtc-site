import React, { Component } from 'react';
import {Main} from "./main/Main";

class App extends Component {
    render() {
        return <Main titles={this.props.payload.titles} pages_count={this.props.payload.titles_count} />;
    }
}

export { App };

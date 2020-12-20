import React, { Component } from 'react';

class Pages extends Component {
    render() {
        const { pages_count } = this.props;

        return <div>
            {
                (new Array(pages_count)).fill(null).map((val, index) => {
                    return <span key={index} className="page-ref">
                      <a href={`/page/${index}`}>
                        {index + 1}
                      </a>
                    </span>;
                })
            }
        </div>;
    }
}

export { Pages };

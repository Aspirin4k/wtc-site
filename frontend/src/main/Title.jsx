import React, { Component } from 'react';

class Title extends Component {
    render() {
        const { title, isFirst, isLast } = this.props;
        const hasImage = !!title.url;
        return <a href={`/post/${title.vk_id}`}>
            <div className={'title-post' + (isFirst ? ' title-post_first' : '') + (isLast ? ' title-post_last' : '')}>
                {
                    hasImage &&
                    <div className="title-post-preview">
                        <img src={title.url} className="title-post-preview-img"/>
                    </div>
                }
                <div className="title-post-info">
                    <h2 className="title-post-info-header">{ title.title }</h2>
                    <p className="title-post-info-text">{ title.text }</p>
                    <span className="title-post-info-shadow" />
                </div>
            </div>
        </a>
    }
}

export { Title };

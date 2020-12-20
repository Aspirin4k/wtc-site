import React, { Component, Fragment } from 'react';
import {Title} from "./Title";
import {Pages} from "./Pages";

class Main extends Component {
    render() {
        const { titles, pages_count } = this.props;

        return <Fragment>
            <div>
                <a href="/"> DOMOI </a>
            </div>
            <Pages pages_count={pages_count} />
            {
                titles.map((title, index) => {
                    return <Title
                        key={title.id}
                        title={title}
                        isFirst={index === 0}
                        isLast={index === titles.length - 1}
                    />
                })
            }
            <Pages pages_count={pages_count} />
            <div id="footer">
                &copy; Все права защищены СНГ сообществом ценителей работ
                Рюкиси07
                <p>
                    Читать посты в формате <a href="/feed.xml"> RSS </a>
                </p>
            </div>
        </Fragment>
    }
}

export { Main };

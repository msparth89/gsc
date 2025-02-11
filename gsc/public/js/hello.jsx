import React from 'react';
import * as ReactDOM from 'react-dom'

class App extends React.Component {
    render() {
        return (
            <div className="App">
                <h1>MaaShakti</h1>
            </div>
        );
    }
}

export default function hello(it) {
    ReactDOM.render(<App/>, it);
}
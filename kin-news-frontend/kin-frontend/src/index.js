import React from 'react';
import {createRoot} from 'react-dom/client';
import './index.css';
import App from './components/App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from "react-router-dom";
import {Provider} from "react-redux";

import store from "./redux/store";

const container = document.getElementById('root')
const root = createRoot(container);

root.render(
    <>
        <React.StrictMode>
            <BrowserRouter>
                <Provider store={store}>
                    <App />
                </Provider>
            </BrowserRouter>
        </React.StrictMode>
    </>
);

reportWebVitals();

import React from 'react';
import { createRoot } from 'react-dom/client';
import './App.css';
import App from './App';

console.log('Index.js loading...');
console.log('React available:', typeof React !== 'undefined');

const container = document.getElementById('root');
if (container) {
    console.log('Root container found, creating React root...');
    const root = createRoot(container);
    root.render(React.createElement(App));
    console.log('React app rendered successfully');
} else {
    console.error('Root container not found!');
}

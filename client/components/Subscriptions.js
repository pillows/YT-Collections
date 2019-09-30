import React, { useEffect, useCallback, useState, useRef } from 'react';
import './Subscriptions.scss';

const Channel = () => {
    return (
        <div className="channel-view">
            <div className="channel-img">
                <img src="https://picsum.photos/200" />
                <button>X</button>
            </div>
            <div className="channel-info">
                <h3>Channel Name</h3>
                <p>Subscribed on 01/01/01</p>
            </div>
        </div>
    )
}

const Subscription = () => {
    return (
        <div className="content">
            <div className="sub-search">
                <input placeholder="Search Subscriptions" />
            </div>
            <h3 style={{textAlign: 'right', color: 'red'}}>Subscription Count: 700</h3>
            <div className="sub-view">
                { Array(20).fill(0).map((val, index) => <Channel key={`index${index}`} />) }
            </div>
        </div>
    );
};

export default Subscription;
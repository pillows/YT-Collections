import React, { useEffect, useCallback, useState, useRef } from 'react';
import './Subscriptions.scss';

const Modal = (props) => {
    const [error, setError] = useState(false);
    const { channel, closeModal, unSubscribe } = props;

    const unSubscribeEvent = async (id) => { await unSubscribe(id) ? setError(false) : setError(true); }
    
    return (
        <div className="modal-content">
            <div className="modal-title">
                <button onClick={closeModal}>X</button>
                <h1>Are you sure ?</h1>
                { error ? <p style={{color: 'red'}}>Unable to Unsubscribe. Try Again Later</p> : null }
            </div>
            <p>Do you want to unsubscribe from {channel.title} ?</p>
            <embed src={channel.thumbnail.url} />
            <div className="modal-options">
                <button onClick={() => unSubscribeEvent(channel.id)}>Yes</button>
                <button onClick={closeModal}>No</button>
            </div>
        </div>
    );
};

const Channel = (props) => {
    const { channel, showModal } = props;
    return (
        <div className="channel">
            <a href={`/channel/${channel.id}`}>
                <div className="channel-img" style={{backgroundImage: `url("${channel.thumbnail.url}")`}}>
                    <button className="delete" onClick={(event) => showModal(event, channel)}>X</button>
                </div>
                <p className="title">{channel.title}</p>
                <hr />
                <div>
                    <p>{channel.sub_count} Subscribers</p>
                    <p>{channel.view_count} Views</p>
                </div>
            </a>
        </div>
    );
};

const Subscription = () => {
    const [channels, setChannels] = useState([...subscriptions]);
    const [page, setPage] = useState(0);
    const [searchFilter, setSearchFilter] = useState('');
    const [modal, setModal] = useState({show: false, channel: null});
    const ref = useRef({search: true, page: true});

    const showModal = (event, channel) => {
        event.preventDefault();
        setModal({show: true, channel});
    }

    const closeModal = () => setModal({show: false, channel: null});

    const unSubscribe = async (id) => {
        try {
            const response = await fetch(`/subscriptions/unsubscribe`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({'channel_id': id})
            });
            if (response.status !== 200) return false;
            closeModal();
            setChannels(channels.filter(val => val.id !== id));
            return true;
        } catch (e) {
            return false;
        }
    }

    const loadNextPage = async (page) => {
        if (page < total_pages) {
            try {
                const response = await fetch(`/subscriptions/page/${page}`);
                if (response.status != 200) {
                    // ADD redirect to error page
                    return false;
                }
                const data = await response.json();
                setChannels([...channels, ...data.subscriptions]);
                return true;
            } catch (e) {
                // ADD redirect to error page
                return false;
            }
        }
        return false;
    };

    const scrollCallback = useCallback(() => {
        if (window.scrollY + window.innerHeight > document.body.clientHeight - 200) setPage(page + 1);
    }, [page]);

    useEffect(() => { 
        if (ref.current.page) { ref.current.page = false; }
        else { loadNextPage(page) }
    }, [page]);

    useEffect(() => {
        const search = async () => {
            let thisPage = page + 1;
            setPage(total_pages);
            while (await loadNextPage(thisPage)) { thisPage += 1; }
        }
        if (ref.current.search) { ref.current.search = false; }
        else { search(); }
    }, [searchFilter])

    useEffect(() => { 
        document.addEventListener('scroll', scrollCallback)
        return () => document.removeEventListener('scroll', scrollCallback);
    });

    const ChannelViews = channels.filter(channel => channel.title.toLowerCase().includes(searchFilter.toLowerCase()))
                                .map(channel => <ChannelView key={channel.id} channel={channel} showModal={showModal} />)

    return (
        <div>
            <div className="search">
                <input placeholder="Search Subscriptions" value={searchFilter} onChange={(e) => setSearchFilter(e.target.value)}/>
                <button>
                    <embed src="https://icon-library.net//images/svg-search-icon/svg-search-icon-15.jpg" />
                </button>
            </div>
            <div className="channel-view">
                { ChannelViews }
            </div>
            { 
                modal.show ? 
                <div className="modal">
                    <ModalView channel={modal.channel} closeModal={closeModal} unSubscribe={unSubscribe} />
                </div>
                :
                null
            }
        </div>
    );
};

export default Subscription;
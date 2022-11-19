import React, {useCallback, useRef} from 'react';
import LoadingSpinner from "../../common/spiner/LoadingSpinner";
import {showModalWindow} from "../../../redux/reducers/modalWindowReducer";
import {addChannel, fetchChannels} from "../../../redux/reducers/channelsReducer";
import {fetchNextPosts} from "../../../redux/reducers/postsReducer";
import {connect} from "react-redux";
import Post from "./post/Post";

const PostsTape = (props) => {
    function truncatePostLink(linkString) {
        let linkParts = linkString.split('/')
        let postId = linkParts[linkParts.length - 1]
        let channelId = linkParts[linkParts.length - 2]

        return `${channelId}/${postId}`
    }

    let observer = useRef()

    // eslint-disable-next-line react-hooks/exhaustive-deps
    let lastUserRef = useCallback(node => {
        if(observer.current) {
            observer.current.disconnect()
        }

        observer.current = new IntersectionObserver(entries => {
            if(entries[0].isIntersecting){
                props.fetchNewPosts()
            }
        })

        if (node) {
            observer.current.observe(node)
        }
    })

    if(props.posts.length === 0) {
        props.fetchNewPosts();
        return (
            <LoadingSpinner width={100} height={100} marginTop={"10%"} />
        )
    }

    return (
        <>
            {
                props.posts.map((el, i) => {
                    if(i === props.posts.length - 1) {
                        return <div ref={lastUserRef} key={i}><Post postLink={truncatePostLink(el.link)} /></div>
                    }
                    else {
                        return <Post postLink={truncatePostLink(el.link)} key={i} />
                    }
                })
            }
        </>
    );
};

let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        fetchNewPosts: () => dispatch(fetchNextPosts()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(PostsTape);
import React, {useEffect} from 'react';

const Post = (props) => {
    const postClassName = props.postLink.replace('/', '-')

    useEffect(() => {
        const script = document.createElement('script');
        script.src = "https://telegram.org/js/telegram-widget.js?21";

        script.setAttribute('data-telegram-post', props.postLink)

        script.setAttribute('data-dark-color', 'F95C54')
        script.setAttribute('data-userpic', 'true')
        script.setAttribute('data-color', 'E22F38')
        script.setAttribute('data-dark', '1')
        script.async = true;

        document.querySelector(`.${postClassName}`).appendChild(script);
    }, [props.postLink])

    return (
        <div className={postClassName}></div>
    );
};

export default Post;
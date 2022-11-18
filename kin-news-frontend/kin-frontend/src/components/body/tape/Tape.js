import {useEffect, useState} from "react";
import TapeCss from "./Tape.module.css"
import Post from "./post/Post";
import {login} from "../../../redux/reducers/authReducer";
import {connect} from "react-redux";
import {showModalWindow} from "../../../redux/reducers/modalWindowReducer";
import Input from "../../common/input/Input";
import Button from "../../common/button/Button";
import {addChannel} from "../../../redux/reducers/channelsReducer";


const EnterLink = (props) => {
    const [link, setLink] = useState({link: ''})

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h4>
                PROVIDE A LINK TO THE CHANNEL
            </h4>
            <Input
                value={link.link}
                onChange={(event) => setLink({link: event.target.value})}
                placeholder={"Channel link"}
            />

            <Button
                text={"Subscribe"}
                onClick={(event) => props.addChannel(link.link)}
            />
        </div>
    )
}


const Tape = (props) => {
    return (
        <div className={TapeCss.container}>
            <div className={TapeCss.sideBar}>
                <div className={TapeCss.sideBarContent}>
                    <div
                        className={TapeCss.addChannelButton}
                        onClick={() => props.showModal(<EnterLink addChannel={props.addChannel} />, 400, 300)}
                    >
                        SUBSCRIBE
                    </div>

                </div>
            </div>
            <div className={TapeCss.tape}>
                <Post postLink={"ukraina_novosti/43990"} />
                <Post postLink={"ukraina_novosti/43991"} />
                <Post postLink={"ukraina_novosti/43992"} />
                <Post postLink={"ukraina_novosti/43993"} />
            </div>
        </div>
    )
}

let mapStateToProps = (state) => {
    return {
        channels: state.channels.channels,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        addChannel: (link) => dispatch(addChannel(link))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Tape);

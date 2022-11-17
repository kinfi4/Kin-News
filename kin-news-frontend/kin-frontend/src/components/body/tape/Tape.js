import {useEffect} from "react";
import TapeCss from "./Tape.module.css"
import Post from "./post/Post";

const Tape = () => {
    return (
        <div className={TapeCss.tape}>
            <Post postLink={"ukraina_novosti/43990"} />
            <Post postLink={"ukraina_novosti/43991"} />
            <Post postLink={"ukraina_novosti/43992"} />
            <Post postLink={"ukraina_novosti/43993"} />
        </div>
    )
}

export default Tape;

import defaultButtonCss from './Button.module.css'


function Button(props) {
    return (
        <>
            <div
                className={defaultButtonCss.defaultButton}
                onClick={(event) => props.onClick(event)}
            >
                { props.text }
            </div>
        </>
    )
}


export default Button;
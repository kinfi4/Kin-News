import inputCss from './Input.module.css'


function Input(props) {
    return (
        <>
            <input
                className={inputCss.defaultInput}
                type={props.type ? props.type : "text"}
                onChange={(e => props.onChange(e))}
                value={props.value}
                placeholder={props.placeholder}
                id={props.id}
            />
        </>
    )
}

export default Input;
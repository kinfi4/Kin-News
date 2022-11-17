import {Store} from "react-notifications-component";

export let showMessage = (messages) => {
    messages.forEach(el => {
        Store.addNotification({
            title: '',
            message: el.message,
            type: el.type,                           // 'default', 'success', 'info', 'warning'
            container: 'top-right',                  // where to position the notifications
            animationIn: ["animated", "fadeIn"],
            animationOut: ["animated", "fadeOut"],
            dismiss: {
                duration: 10000
            }
        })
    })
}

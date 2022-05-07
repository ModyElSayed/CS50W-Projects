import {getCookie} from "./utilities.js";

export async function update_or_new_post(new_content, old_content='', post_id='', status='New') {
    let csrftoken = getCookie('csrftoken')
    await fetch(`/update_or_new_post/`, {
        method: status === 'Update' ? 'PUT' : 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            new_content: new_content,
            old_content: old_content,
            post_id: post_id
        })
    })
     .then(response => response.json())
     .then(message => {
         console.log(message.message);
     });
}
import {add_comment_container, getCookie} from "./utilities.js";

export async function add_comment(post_id, comment_content) {
    let csrftoken = getCookie('csrftoken')
    return  fetch(`/add_comment/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            post_id: post_id,
            comment_content: comment_content
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
}

export async function update_comments_section(post_id) {
    await fetch(`/get_last_comment/${post_id}`, {
       method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        add_comment_container(data.comment, post_id);
    });
}
import {getCookie} from "./utilities.js";

export async function check_if_liked() {
    await fetch('/check_likes/', {
        method: 'GET'
    })
    .then(response => response.json()).then(data => {
        data.posts_id.forEach(post => {
           document.querySelector(`#heart_${post}`).className = 'bi bi-heart-fill text-danger';
        });
    });
}

export function update_num_of_likes(post_id) {
    let csrftoken = getCookie('csrftoken')
    return  fetch(`/update_likes/`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            post_id: post_id
        })
    })
    .then(response => response.text()) // Parse the response as text
    .then(text => {
        try {
            const data = JSON.parse(text); // Try to parse the response as JSON
            console.log(data.message);
            document.querySelector(`#num-of-likes_${post_id}`).innerHTML = data.number_of_likes;
            document.querySelector(`#heart_${post_id}`).className = data.status === 'Increased' ? 'bi bi-heart-fill text-danger' : 'bi bi-heart text-danger';
        } catch (err) {
            return text;
        }
    });
}

import {getCookie} from "./utilities.js";

export async function update_follower(follower, status) {
    let csrftoken = getCookie('csrftoken')
    await fetch(`/update_follower/`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify({
            follower: follower,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        const check_follow_text = document.querySelector('#follow-button').innerHTML;
        if (check_follow_text === 'Follow') {
            document.querySelector('#follow-button').innerHTML = 'Unfollow';
            document.querySelector('#follow-button').className = 'btn btn-outline-primary m-3';
        } else {
            document.querySelector('#follow-button').innerHTML = 'Follow';
            document.querySelector('#follow-button').className = 'btn btn-primary m-3';
        }
        document.querySelector('#follow-data').innerHTML = `<strong>Followers: </strong>${data.number_of_followers} <strong>Following: </strong>${data.number_of_following}`
    });

}
import {update_or_new_post} from "./posts.js";

export function edit_post_content(edit_post_button) {
    let post_content = edit_post_button.parentElement.childNodes[3];
    let textarea_div_container = document.createElement('div');
    let textarea_for_edit = document.createElement('textarea');
    let textarea_label = document.createElement('label');

    localStorage.setItem('old_post_content', post_content.innerHTML);

    textarea_div_container.className = "form-floating m-3";
    textarea_div_container.id = "edit-post-container";
    textarea_for_edit.id = "edit-post-content";
    textarea_for_edit.placeholder = "Edit Content";
    textarea_for_edit.value = post_content.innerHTML;
    textarea_for_edit.className = "form-control";
    textarea_label.htmlFor = "edit-post-content";
    textarea_label.className = "text-muted";
    textarea_label.innerText = "Edit Content";

    textarea_div_container.append(textarea_for_edit, textarea_label);
    post_content.parentNode.replaceChild(textarea_div_container, post_content);
    edit_post_button.innerHTML = "Save";
}

export async function save_edited_post(edit_post_button) {

    let textarea_div_container;
    edit_post_button.parentNode.childNodes.forEach(item => {
        if (item.id !== undefined && item.id.includes('edit-post-container')) {
            textarea_div_container = item;

        }
    });
    let textarea_for_edit = textarea_div_container.firstChild;
    let post_content = document.createElement('p');
    post_content.innerHTML = textarea_for_edit.value;
    post_content.className = "ms-3 mt-3";

    let post_id;
    edit_post_button.parentNode.childNodes.forEach(item => {
        if (item.type === 'hidden' && item.id.includes('post-')) {
            post_id = item.value;
        }
    });

    await update_or_new_post(post_content.innerHTML, localStorage.getItem('old_post_content'), post_id, 'Update');
    localStorage.removeItem('old_post_content');

    textarea_div_container.parentNode.replaceChild(post_content, textarea_div_container);
    edit_post_button.innerHTML = "Edit";

    document.querySelectorAll('.post-container').forEach(container => container.childNodes.forEach(item => {
        if (item.className !== undefined && item.className.includes('error-edit')) {
            item.innerText = '';
        }
    }));
}

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function add_comment_container(comment, post_id) {
    let comment_container = document.createElement('div');
    comment_container.className = 'm-3 rounded border comment-container';

    let username = document.createElement('p');
    username.className = 'fw-bolder m-3 fs-5';

    let username_link = document.createElement('a');
    username_link.className = 'text-decoration-none text-dark';
    username_link.href = `/profile/${comment.username}`;
    username_link.innerHTML = `${comment.username}`;

    username.append(username_link);

    let content = document.createElement('p');
    content.className = 'ms-3 mt-3';
    content.innerHTML = `${comment.content}`;

    let date_created = document.createElement('time');
    date_created.className = 'ms-3 mb-3 text-muted';
    date_created.innerHTML = `${comment.date_created}`;

    let date_created_margin = document.createElement('div');
    date_created_margin.className = 'm-3';

    let comment_data = document.createElement('input');
    comment_data.type = 'hidden';
    comment_data.value = post_id;
    comment_data.id = `comment-${comment.comment_id}`;

    comment_container.append(username, content, date_created, date_created_margin, comment_data);

    let comment_section = document.querySelector(`#post-comment-${post_id}`);
    comment_section.prepend(comment_container);
}

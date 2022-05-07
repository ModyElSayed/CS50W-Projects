import {update_follower} from "./profile.js";
import {add_comment, update_comments_section} from "./comments.js";
import {check_if_liked, update_num_of_likes} from "./likes.js";
import {update_or_new_post} from "./posts.js";
import {edit_post_content, save_edited_post} from "./utilities.js";

document.addEventListener('DOMContentLoaded', async function () {

        if (document.querySelector('#page').value === 'index' && document.querySelector('#login-status').value === "True") {
            document.querySelector('#new-post-content').addEventListener('keyup', function () {
                document.querySelector('#submit-post').disabled = document.querySelector('#new-post-content').value.length <= 0;
            });

            document.querySelector('#new-post').addEventListener('submit', async () => {
                if (document.querySelector('#new-post-content').value.length > 0) {
                    await update_or_new_post(document.querySelector('#new-post-content').value);
                }
            });
        }

        if (document.querySelector('#page').value === 'profile' && document.querySelector('#login-status').value === "True") {
            if (document.querySelector('#login-username').value !== document.querySelector('#profile-username').innerHTML) {
                document.querySelector('#follow-button').addEventListener('click', async () => {
                    let status = document.querySelector('#follow-button').innerHTML;
                    let follower = document.querySelector('#profile-username').innerHTML;

                    await update_follower(follower, status);
                });
            }
        }

        if (document.querySelector('#login-status').value === 'True') {
            await check_if_liked();
        }

        document.addEventListener('click', async function (event) {
            let is_post_edit = false;
            let edit_post_button = event.target;

            if (event.target.innerHTML === 'Edit') {
                document.querySelectorAll('.edit-post').forEach(button => {
                    if (button.innerHTML === 'Save') {
                        is_post_edit = true;
                    }
                });
            }

            if (is_post_edit) {
                edit_post_button.parentElement.childNodes.forEach(item => {
                    if (item.className !== undefined && item.className.includes('error-edit')) {
                        item.innerText = "Save the post you are editing first";
                    }
                });
            } else {
                if (edit_post_button.innerHTML === 'Edit') {
                    edit_post_content(edit_post_button);

                } else if (edit_post_button.innerHTML === 'Save') {
                    await save_edited_post(edit_post_button);
                }
            }

            if (event.target.id.includes('appear-comment')) {
                let comment = event.target;
                let comment_section = comment.parentNode.lastElementChild;

                comment.innerHTML = 'Comment';

                if (comment_section.style.display === 'block') {
                    comment_section.style.display = 'none';
                } else if (comment_section.style.display === 'none') {
                    comment_section.style.display = 'block';
                }
            }

            if (document.querySelector('#login-status').value === 'True' && event.target.parentNode.className.includes('likes')) {
                event.target.parentNode.parentNode.childNodes.forEach(item => {
                    if (item.type === 'hidden' && item.id.includes('post-')) {
                        update_num_of_likes(item.value);
                    }
                });

            }

            if (document.querySelector('#login-status').value === 'True' && event.target.id.includes('add-comment-')) {
                let add_comment_button = event.target;
                let comment_content = add_comment_button.parentNode.firstElementChild;
                let post_id = add_comment_button.id.split('-')[2];

                if (comment_content.value !== '') {
                    await add_comment(post_id, comment_content.value);
                    await update_comments_section(post_id);

                    comment_content.value = '';

                    let show_comments = document.querySelector(`#post-comment-${post_id}`);
                    if (show_comments.style.display === 'none') {
                        show_comments.style.display = 'block';
                    }
                } else {
                    comment_content.required = true;
                }
            }

            let button_class = event.target.parentNode.className;
            if (document.querySelector('#login-status').value === 'False' && (button_class.includes('likes') || button_class.includes('add-comment-')) &&
                !location.href.includes('login/')) {
                location.href = "login/"
            }
        });

        document.addEventListener('keyup', (event) => {
           if (event.target.id.includes('comment-content')) {
                let comment_area = event.target;
                comment_area.parentNode.lastElementChild.disabled = comment_area.value.length <= 0;
            }
        });
});
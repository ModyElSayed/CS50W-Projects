import { view_mailbox } from "./inbox.js";

export async function archive_email(email_id, mailbox) {
    await fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: mailbox === 'inbox'
        })
    });

    view_mailbox('inbox');
}

export function read_email(email_id) {
     return fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    });
}
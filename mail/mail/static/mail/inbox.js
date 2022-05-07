import { load_mailbox, email_preview } from './utilities.js';
import { compose_email } from './compose.js';
import { sent_email } from './sent.js';
import { archive_email } from "./email_status.js";

document.addEventListener('DOMContentLoaded', function() {

  // By default, load the inbox
  view_mailbox('inbox');

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => view_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => view_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => view_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#submit-email').addEventListener('click', () => view_mailbox('submit'));

  document.addEventListener('click', function (event) {
    const element = event.target;
    if (element.className.includes('hide')) {
        element.parentElement.style.animationPlayState = "running";
        element.parentElement.addEventListener('animationend', () => {
           element.parentElement.remove();
           return archive_email(element.parentElement.dataset.id, element.parentElement.dataset.mailbox);
        });
    }
  });

});

export function view_mailbox(mailbox) {
    load_mailbox(mailbox);

    if (mailbox === 'submit') {
        sent_email();
        mailbox = 'sent';
    }

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {
            email_preview(email, mailbox);
        });
    });
}
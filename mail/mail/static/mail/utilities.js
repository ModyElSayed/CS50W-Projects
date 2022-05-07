import {read_email} from './email_status.js';
import {compose_reply} from "./compose.js";

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function load_email_content() {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'block';
}

function email_preview(email, mailbox) {
    const email_container = document.createElement('div')
    email_container.className = "container border archive rounded center-block m-1 mt-3 row";
    email_container.id = "email_container";
    email_container.dataset.id = email.id;
    email_container.dataset.mailbox = mailbox;
    email_container.style.background = email.read ? '#B7B7B7' : 'white';

    const email_address = document.createElement('button');
    email_address.className = "fs-5 fw-bold col-auto mt-3 text-black";
    email_address.style.background = 'white';
    email_address.style.borderWidth = '0px';
    email_address.style.height = "50%";
    email_address.style.background = email.read ? '#B7B7B7' : 'white';
    email_address.onclick = function () {
        return view_email_content(email);
    };

    const subject = document.createElement('p');
    subject.className = "fs-5 mt-3 col";
    subject.innerText = email.subject;

    const time = document.createElement('time');
    time.className = "mt-3 left col-auto";
    time.className.concat(email.read ? "" : " text-muted");
    time.innerText = email.timestamp;

    const id = document.createElement('input');
    id.value = email.id;
    id.type = "hidden";

    let archive;
    if (mailbox === 'sent') {
        email_address.innerText = email.recipients;
        email_container.append(email_address, subject, time, id);

    } else {
        email_address.innerText = email.sender;

        archive = document.createElement('button');
        archive.className = "btn btn-primary mt-2 hide col-auto";
        archive.style.height = "40%";
        archive.innerText = mailbox === 'archive' ? "Unarchive" : "Archive";

        email_container.append(email_address, subject, time, archive, id);
    }

    document.querySelector('#emails-view').append(email_container);
}

function view_email_content(email) {
    document.querySelector('#email-content').lastChild.remove();

    const email_content_container = document.createElement('div');

    const sender = document.createElement('p');
    sender.className = "fs-5";
    sender.innerHTML = '<strong>From: </strong>' + email.sender;

    const receiver = document.createElement('p');
    receiver.className = "fs-5";
    receiver.innerHTML = '<strong>To: </strong>' + email.recipients;

    const subject = document.createElement('p');
    subject.className = "fs-5";
    subject.innerHTML = '<strong>Subject: </strong>' + email.subject;

    const timestamp = document.createElement('p');
    timestamp.className = "fs-5";
    timestamp.innerHTML = '<strong>Timestamp: </strong>' + email.timestamp;

    const reply = document.createElement('button');
    reply.innerText = "Reply";
    reply.className = "btn btn-sm btn-outline-primary fs-5 mt-2";
    reply.addEventListener('click', function () {
        compose_reply(email);
    });

    const line_breaker = document.createElement('hr');

    const body = document.createElement('p');
    body.innerText = email.body;

    email_content_container.append(sender, receiver, subject, timestamp, reply, line_breaker, body);
    document.querySelector("#email-content").append(email_content_container);

    load_email_content();

    return read_email(email.id);
}

export { load_mailbox, email_preview, view_email_content };